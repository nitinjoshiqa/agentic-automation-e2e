#!/usr/bin/env python3
"""
Complete end-to-end demo runner for agentic automation workflow.
Flow: requirement -> feature files -> page objects -> test execution -> report generation
"""
import os
import sys
import json
import subprocess
import time
from pathlib import Path

def log(msg, level='INFO'):
    print(f"[{level}] {msg}")

def run_cmd(cmd, shell=False, capture=False, cwd=None):
    """Run a command and return exit code + output"""
    try:
        if capture:
            result = subprocess.run(cmd, shell=shell, capture_output=True, text=True, cwd=cwd, timeout=60)
            return result.returncode, result.stdout + result.stderr
        else:
            result = subprocess.run(cmd, shell=shell, cwd=cwd, timeout=60)
            return result.returncode, ""
    except Exception as e:
        return 1, str(e)

def check_python():
    """Check if Python is available"""
    code, out = run_cmd([sys.executable, '--version'], capture=True)
    if code == 0:
        log(f"Python available: {out.strip()}")
        return True
    else:
        log("Python not found in PATH", 'ERROR')
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        resp = requests.post('http://localhost:11434/api/generate',
                            json={'model': 'mistral', 'prompt': 'test', 'max_tokens': 5},
                            timeout=3)
        log(f"Ollama reachable: status {resp.status_code}")
        return resp.status_code in [200, 201]
    except Exception as e:
        log(f"Ollama check failed: {e}", 'WARN')
        return False

def setup_venv(venv_path):
    """Create and activate venv, install dependencies"""
    log(f"Setting up venv at {venv_path}")

    # Create venv
    code, _ = run_cmd([sys.executable, '-m', 'venv', str(venv_path)], capture=True)
    if code != 0:
        log("Failed to create venv", 'ERROR')
        return False

    # Get pip path
    if sys.platform == 'win32':
        pip_exe = venv_path / 'Scripts' / 'python.exe'
    else:
        pip_exe = venv_path / 'bin' / 'python'

    # Upgrade pip
    log("Upgrading pip...")
    run_cmd([str(pip_exe), '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'], capture=True)

    # Install packages
    log("Installing dependencies...")
    packages = [
        'fastapi==0.95.2',
        'uvicorn[standard]==0.22.0',
        'langchain==0.0.300',
        'sentence-transformers==2.2.2',
        'requests==2.31.0',
        'pydantic==2.5.2',
        'PyYAML==6.0',
        'chromadb==0.3.26',
    ]
    code, out = run_cmd([str(pip_exe), 'install'] + packages, capture=True)
    if code != 0:
        log(f"Pip install failed:\n{out}", 'WARN')
        return False

    log("Venv setup complete")
    return True

def run_generation(rag_module_path, requirement, module='demo'):
    """Run the RAG generation flow"""
    log(f"Running generation for: {requirement}")

    # Try to import and run RAGService
    sys.path.insert(0, str(rag_module_path.parent))
    try:
        from agent_service.rag import RAGService
        rag = RAGService()

        log("RAGService initialized (real LLM path)")
        features = rag.generate_features(requirement_text=requirement, module=module)
        log(f"Features generated: {len(features.get('written_features', []))} files")

        page_hints = features.get('page_hints', [])
        if page_hints:
            pages = rag.generate_pages(page_hints=page_hints, module=module)
            log(f"Pages generated: {len(pages.get('written_pages', []))} files")
            return {
                'mode': 'real_llm',
                'written_features': features.get('written_features', []),
                'written_pages': pages.get('written_pages', [])
            }
        else:
            log("No page hints returned", 'WARN')
            return {'mode': 'real_llm', 'written_features': features.get('written_features', []), 'written_pages': []}

    except Exception as e:
        log(f"RAGService failed: {e}", 'WARN')
        log("Falling back to quick generator", 'INFO')
        try:
            from agent_service.quick_demo import write_feature, write_pages
            feat = write_feature(module)
            pages = write_pages(module)
            return {
                'mode': 'fallback',
                'written_features': [os.path.abspath(feat)],
                'written_pages': [os.path.abspath(p) for p in pages]
            }
        except Exception as e2:
            log(f"Fallback also failed: {e2}", 'ERROR')
            return None

def run_tests(repo_root):
    """Run Maven tests"""
    log("Running tests via Maven...")
    code, out = run_cmd(['mvn', 'clean', 'verify'], capture=True, cwd=str(repo_root))
    if code == 0:
        log("Tests passed")
        return True, out
    else:
        log(f"Tests failed or had issues:\n{out[:1000]}", 'WARN')
        return False, out

def generate_report(repo_root):
    """Generate Allure report"""
    log("Generating Allure report...")
    code, out = run_cmd(['mvn', 'allure:report'], capture=True, cwd=str(repo_root))
    if code == 0:
        log("Report generated")
        return True
    else:
        log(f"Report generation had issues:\n{out[:500]}", 'WARN')
        return False

def main():
    log("=== Agentic Automation Workflow Demo ===")

    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent  # reflectioncucumber/
    agent_service_dir = script_dir.parent  # agent-service/
    venv_path = agent_service_dir / '.venv'

    log(f"Repo root: {repo_root}")
    log(f"Agent service: {agent_service_dir}")

    # Step 1: Check Python
    log("Step 1: Checking Python...")
    if not check_python():
        log("Python not available; cannot proceed", 'ERROR')
        return False

    # Step 2: Check Ollama (optional)
    log("Step 2: Checking Ollama...")
    ollama_available = check_ollama()
    if ollama_available:
        log("Ollama available - will use real LLM")
    else:
        log("Ollama not available - will use fallback generator")

    # Step 3: Setup venv
    log("Step 3: Setting up Python environment...")
    if not venv_path.exists():
        if not setup_venv(venv_path):
            log("Venv setup failed", 'ERROR')
            return False
    else:
        log("Venv already exists")

    # Step 4: Generate features and pages
    log("Step 4: Generating features and page objects...")
    requirement = "As a user I want to log in with username and password so I can access my inventory"
    gen_result = run_generation(script_dir, requirement, module='agentic_demo')
    if not gen_result:
        log("Generation failed", 'ERROR')
        return False

    log(f"Generation mode: {gen_result['mode']}")
    log(f"Features: {gen_result['written_features']}")
    log(f"Pages: {gen_result['written_pages']}")

    # Step 5: Run tests
    log("Step 5: Running tests...")
    test_ok, test_out = run_tests(repo_root)

    # Step 6: Generate report
    log("Step 6: Generating report...")
    report_ok = generate_report(repo_root)

    # Summary
    log("\n=== DEMO SUMMARY ===")
    log(f"Generation: SUCCESS ({gen_result['mode']})")
    log(f"Tests: {'SUCCESS' if test_ok else 'ISSUES (see logs)'}")
    log(f"Report: {'SUCCESS' if report_ok else 'FAILED'}")
    log(f"\nGenerated features: {len(gen_result['written_features'])} files")
    log(f"Generated pages: {len(gen_result['written_pages'])} files")
    log(f"\nFeature files location: {repo_root / 'src' / 'test' / 'resources' / 'features' / 'agentic_demo'}")
    log(f"Page objects location: {repo_root / 'src' / 'main' / 'java' / 'org' / 'example' / 'pages' / 'agentic_demo'}")
    log(f"Report location: {repo_root / 'target' / 'allure-report' / 'index.html'}")

    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

