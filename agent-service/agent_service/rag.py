import os
import yaml
import json
from typing import List

from langchain.document_loaders import TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import Ollama

from .prompts import FEATURE_SYSTEM_PROMPT, PAGE_OBJECT_SYSTEM_PROMPT, ANALYSIS_SYSTEM_PROMPT

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')
with open(CONFIG_PATH, 'r') as f:
    CONFIG = yaml.safe_load(f)


class RAGService:
    def __init__(self):
        self.config = CONFIG
        self.top_k = self.config.get('rag', {}).get('top_k', 6)
        self.chunk_size = self.config.get('rag', {}).get('chunk_size', 1000)
        self.chunk_overlap = self.config.get('rag', {}).get('chunk_overlap', 200)

        # Embeddings
        emb_model = self.config.get('embeddings', {}).get('model', 'all-MiniLM-L6-v2')
        self.embeddings = HuggingFaceEmbeddings(model_name=emb_model)

        # Vectorstore
        vs_path = os.path.join(os.path.dirname(__file__), self.config.get('vectorstore', {}).get('path', './knowledge/index'))
        os.makedirs(vs_path, exist_ok=True)
        self.vectorstore = Chroma(persist_directory=vs_path, embedding_function=self.embeddings)

        # LLM: Ollama - local
        llm_model = self.config.get('llm', {}).get('model', 'mistral')
        llm_addr = self.config.get('llm', {}).get('address', 'http://localhost:11434')
        try:
            self.llm = Ollama(url=llm_addr, model=llm_model)
        except Exception as e:
            print('Warning: Ollama LLM initialization failed:', e)
            self.llm = None

    def ingest_directory(self, path: str):
        """Ingest files from a directory into the vectorstore"""
        loader = DirectoryLoader(path, glob='**/*.*', loader_cls=TextLoader)
        docs = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        chunks = text_splitter.split_documents(docs)

        self.vectorstore.add_documents(chunks)
        self.vectorstore.persist()
        return {'added_chunks': len(chunks)}

    def retrieve(self, query: str, top_k: int = None):
        k = top_k or self.top_k
        results = self.vectorstore.similarity_search(query, k=k)
        return results

    def generate_features(self, requirement_text: str, module: str = 'generated'):
        # Retrieve context
        hits = self.retrieve(requirement_text)
        context = '\n\n'.join([h.page_content for h in hits])

        system = FEATURE_SYSTEM_PROMPT
        prompt = f"{system}\n\nCONTEXT:\n{context}\n\nREQUIREMENT:\n{requirement_text}\n\nProduce JSON output as specified."

        if self.llm:
            resp = self.llm(prompt)
            text = resp
        else:
            # Simple fallback: echo a small feature based on requirement
            text = json.dumps({
                'features': [
                    {'filename': f'{module}/Generated.feature', 'content': f'Feature: Generated from requirement\n  Scenario: Auto\n    When I enter "standard_user" in "username" in "LoginPage"\n    And I enter "secret_sauce" in "password" in "LoginPage"\n    And I click "loginButton" on "LoginPage"\n    Then "inventoryContainer" should be displayed on "InventoryPage"'}
                ],
                'page_hints': [
                    {'page': 'LoginPage', 'elements': [{'name': 'username', 'hint': 'username field'}, {'name': 'password', 'hint': 'password field'}, {'name': 'loginButton', 'hint': 'login button'}]}
                ]
            })

        try:
            parsed = json.loads(text)
        except Exception:
            # try to extract json from text
            try:
                start = text.find('{')
                parsed = json.loads(text[start:])
            except Exception as e:
                raise RuntimeError('Failed to parse LLM output as JSON: ' + str(e) + '\nLLM output:\n' + text)

        # write features to repo
        written_files = []
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'test', 'resources', 'features', module))
        os.makedirs(base_path, exist_ok=True)
        for feat in parsed.get('features', []):
            fname = feat.get('filename')
            if '/' in fname:
                fname = fname.split('/')[-1]
            path = os.path.join(base_path, fname)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(feat.get('content'))
            written_files.append(path)

        return {'written_features': written_files, 'page_hints': parsed.get('page_hints', [])}

    def generate_pages(self, page_hints: List[dict], module: str = 'generated', use_scanner: bool = False, site_url: str = None):
        written_files = []
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'main', 'java', 'org', 'example', 'pages', module))
        os.makedirs(base_path, exist_ok=True)

        # Optionally perform a headless scan to get real locators
        scanner_results = {}
        if use_scanner and site_url:
            try:
                from .tools import scan_locators
                all_hints = []
                for ph in page_hints:
                    for e in ph.get('elements', []):
                        all_hints.append({'name': e.get('name'), 'hint': e.get('hint')})
                scanner_results = scan_locators(site_url, hints=all_hints)
            except Exception as e:
                print('Scanner failed:', e)
                scanner_results = {}

        for ph in page_hints:
            page = ph.get('page')
            elements = ph.get('elements', [])

            # If scanner found candidates, choose the top candidate for each element
            if scanner_results:
                for e in elements:
                    name = e.get('name')
                    candidates = scanner_results.get(name) or scanner_results.get('all_inputs') or []
                    if candidates:
                        # pick best candidate
                        best = max(candidates, key=lambda x: x.get('score', 0))
                        # store chosen selector in element for use downstream
                        e['chosen_selector'] = best

            # Build a prompt
            system = PAGE_OBJECT_SYSTEM_PROMPT
            el_text = '\n'.join([f"- {e.get('name')}: {e.get('hint')}" for e in elements])
            prompt = f"{system}\n\nPAGE: {page}\nELEMENTS:\n{el_text}\n\nGenerate the Java class code only. If chosen_selector is provided use that selector as the locator."

            if self.llm:
                resp = self.llm(prompt)
                class_code = resp
            else:
                # fallback: use chosen_selector if present else simple id-based selectors
                field_lines = []
                for e in elements:
                    chosen = e.get('chosen_selector')
                    if chosen:
                        sel = chosen.get('selector')
                        # convert candidate to By.* expression roughly
                        if chosen.get('type') == 'id' and sel.startswith('#'):
                            val = sel[1:]
                            line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.id("' + val + '");'
                        elif chosen.get('type') == 'name' and sel.startswith('[name='):
                            val = sel.split('=')[1].strip("']\"")
                            line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.name("' + val + '");'
                        elif chosen.get('type') == 'css':
                            val = sel
                            line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.cssSelector("' + val + '");'
                        elif chosen.get('type') == 'xpath':
                            val = sel
                            line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.xpath("' + val + '");'
                        else:
                            # fallback to css
                            line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.cssSelector("' + sel + '");'
                    else:
                        line = '    public static final org.openqa.selenium.By ' + e.get('name').upper() + ' = org.openqa.selenium.By.id("' + e.get('name') + '");'
                    field_lines.append(line)

                fields = '\n\n'.join(field_lines)
                class_code = (
                    'package org.example.pages.' + module + ';\n\n'
                    'import org.example.base.BasePage;\n'
                    'import org.openqa.selenium.By;\n'
                    'import org.openqa.selenium.WebDriver;\n\n'
                    'public class ' + page + ' extends BasePage {\n\n'
                    + fields + '\n\n'
                    '    public ' + page + '(WebDriver driver) {\n'
                    '        super(driver);\n'
                    '    }\n'
                    '}\n'
                )

            # write to file
            path = os.path.join(base_path, f"{page}.java")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(class_code)
            written_files.append(path)

        return {'written_pages': written_files}

    def dedupe_pages(self, module: str = 'generated'):
        """Scan existing pages and deduplicate locators between newly generated module and existing pages.
        Returns a report of duplicates and suggested canonicalizations.
        """
        report = {'duplicates': []}
        base_existing = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'main', 'java', 'org', 'example', 'pages'))
        base_new = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src', 'main', 'java', 'org', 'example', 'pages', module))

        def parse_locators(file_path):
            locators = {}
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # crude parse: find lines with "public static final" and extract NAME and selector
                for line in content.splitlines():
                    if 'public static final' in line and '=' in line:
                        parts = line.strip().split()
                        # expecting: public static final By NAME = By.id("...");
                        try:
                            name = parts[4]
                            rhs = line.split('=')[1].strip().rstrip(';')
                            locators[name] = rhs
                        except Exception:
                            continue
            except FileNotFoundError:
                pass
            return locators

        # collect existing locators
        existing = {}
        for root, dirs, files in os.walk(base_existing):
            for f in files:
                if f.endswith('.java'):
                    p = os.path.join(root, f)
                    existing[p] = parse_locators(p)

        # collect new locators
        new = {}
        for root, dirs, files in os.walk(base_new):
            for f in files:
                if f.endswith('.java'):
                    p = os.path.join(root, f)
                    new[p] = parse_locators(p)

        # find duplicates by selector string
        selector_map = {}
        for p, locs in {**existing, **new}.items():
            for name, rhs in locs.items():
                selector_map.setdefault(rhs, []).append({'file': p, 'name': name})

        for selector, items in selector_map.items():
            if len(items) > 1:
                report['duplicates'].append({'selector': selector, 'occurrences': items})

        return report

    def analyze_failure(self, failure_log: str, top_k: int = 6):
        """Analyze failure log using RAG: retrieve similar failures and propose fixes."""
        # Retrieve similar failure context
        hits = self.retrieve(failure_log, top_k=top_k)
        context = '\n\n'.join([h.page_content for h in hits])

        system = ANALYSIS_SYSTEM_PROMPT
        prompt = f"{system}\n\nCONTEXT:\n{context}\n\nFAILURE_LOG:\n{failure_log}\n\nProvide JSON output."

        if self.llm:
            resp = self.llm(prompt)
            text = resp
        else:
            # fallback heuristic
            if 'NoSuchElementException' in failure_log:
                hypothesis = 'Locator missing or changed on the page.'
                fixes = [{'type': 'locator_update', 'suggestion': 'Update locator to use a stable id or css selector', 'confidence': 0.6}]
                next_steps = ['Run headless scanner to find current locator candidates', 'Update page object and rerun tests']
                out = {'hypothesis': hypothesis, 'fixes': fixes, 'next_steps': next_steps, 'confidence': 0.6}
                return out
            else:
                return {'hypothesis': 'Unknown failure pattern', 'fixes': [], 'next_steps': ['Inspect logs manually'], 'confidence': 0.2}

        try:
            parsed = json.loads(text)
        except Exception:
            try:
                start = text.find('{')
                parsed = json.loads(text[start:])
            except Exception as e:
                raise RuntimeError('Failed to parse analysis from LLM: ' + str(e) + '\nLLM output:\n' + text)

        return parsed

