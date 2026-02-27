import subprocess
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


def run_maven_clean_verify(repo_root):
    mvn_cmd = f'mvn -f "{repo_root}" clean verify'
    proc = subprocess.Popen(mvn_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return proc.returncode, out.decode('utf-8', errors='ignore'), err.decode('utf-8', errors='ignore')


def git_commit_and_push(repo_root, branch_name, files, message):
    # Simple git helper (repo must be configured with credentials locally)
    cwd = repo_root
    cmds = [
        f'git checkout -b {branch_name}',
        'git add ' + ' '.join([f'"{f}"' for f in files]),
        f'git commit -m "{message}"',
        f'git push origin {branch_name}'
    ]
    for c in cmds:
        proc = subprocess.Popen(c, cwd=cwd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = proc.communicate()
        if proc.returncode != 0:
            return proc.returncode, out.decode('utf-8'), err.decode('utf-8')
    return 0, 'OK', ''


def scan_locators(url: str, hints: list = None, timeout: int = 10):
    """Headless scan of a page to find candidate locators for element hints.
    hints: list of {'name': 'username', 'hint': 'username field'}
    returns: {hint_name: [ {type: 'id'|'css'|'xpath', 'selector': '...', 'score': 0.9}, ... ]}
    """
    opts = Options()
    opts.headless = True
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    driver.set_page_load_timeout(timeout)

    try:
        driver.get(url)
    except Exception as e:
        driver.quit()
        return {'error': str(e)}

    results = {}

    # If no hints provided, try to scan common interactive elements
    if not hints:
        hints = [{'name': 'all_inputs', 'hint': 'inputs and buttons'}]

    for h in hints:
        name = h.get('name')
        hint = (h.get('hint') or '').lower()
        candidates = []

        # Try finding by id or name from hint
        inputs = driver.find_elements(By.TAG_NAME, 'input') + driver.find_elements(By.TAG_NAME, 'button') + driver.find_elements(By.TAG_NAME, 'a')
        for el in inputs:
            try:
                el_id = el.get_attribute('id')
                el_name = el.get_attribute('name')
                el_class = el.get_attribute('class')
                text = el.text or el.get_attribute('value') or ''
                selector_candidates = []
                if el_id:
                    selector_candidates.append({'type': 'id', 'selector': f"#{el_id}", 'score': 0.95})
                if el_name:
                    selector_candidates.append({'type': 'name', 'selector': f"[name='{el_name}']", 'score': 0.9})
                if el_class:
                    selector_candidates.append({'type': 'css', 'selector': f".{el_class.split()[0]}", 'score': 0.7})
                if text and len(text) < 50:
                    # xpath using text
                    xpath = f"//*[text()='{text}']"
                    selector_candidates.append({'type': 'xpath', 'selector': xpath, 'score': 0.6})

                # heuristic: if hint matches id/name/class/text, boost score
                for c in selector_candidates:
                    s = c['selector'].lower()
                    if hint and hint in s:
                        c['score'] += 0.1

                # add top candidate for this element
                if selector_candidates:
                    # sort by score desc and pick top 1
                    selector_candidates.sort(key=lambda x: -x['score'])
                    candidates.append(selector_candidates[0])
            except Exception:
                continue

        results[name] = candidates

    driver.quit()
    return results
