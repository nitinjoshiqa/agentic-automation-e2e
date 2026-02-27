#!/usr/bin/env python3
"""
RAG Orchestrator - Standalone Script
Run RAG service independent of PowerShell or Copilot
Configures all project info via rag_config.py
"""

import argparse
import requests
import json
import sys
from pathlib import Path
import subprocess
import time

class RAGOrchestrator:
    """Orchestrates RAG service for test generation"""

    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        self.service_process = None

    def start_service(self):
        """Start RAG service"""
        print("\n" + "="*60)
        print("Starting RAG Service...")
        print("="*60)

        try:
            # Check if service is already running
            response = requests.get(f"{self.base_url}/health", timeout=2)
            print(f"[OK] Service already running at {self.base_url}")
            return True
        except:
            # Service not running, start it
            print(f"Starting service on {self.base_url}...")

            rag_file = Path(__file__).parent / "agent_service" / "context_aware_rag.py"
            if not rag_file.exists():
                print(f"[ERROR] RAG service file not found: {rag_file}")
                return False

            # Start service in background
            self.service_process = subprocess.Popen(
                [sys.executable, str(rag_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            # Wait for service to start
            for i in range(30):
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=1)
                    print(f"[OK] Service is ready")
                    print(f"  URL: {self.base_url}")
                    print(f"  PID: {self.service_process.pid}")
                    return True
                except:
                    print(f"  Waiting... ({i+1}/30)")
                    time.sleep(1)

            print("[ERROR] Service failed to start")
            return False

    def list_projects(self):
        """List available projects"""
        try:
            response = requests.get(f"{self.base_url}/projects")
            data = response.json()

            print("\n" + "="*60)
            print("Available Projects")
            print("="*60)

            for project in data.get("projects", []):
                print(f"\nProject: {project['name']}")
                print(f"  Module: {project['module']}")
                print(f"  Site: {project['site_url']}")
                print(f"  Pages: {', '.join(project['pages'])}")

            return True
        except Exception as e:
            print(f"[ERROR] Error listing projects: {e}")
            return False

    def generate_tests(self, requirement, project, module=None):
        """Generate features and pages"""
        try:
            print("\n" + "="*60)
            print("Generating Test Artifacts")
            print("="*60)
            print(f"\nProject: {project}")
            print(f"Requirement: {requirement}\n")

            # Generate features
            print("[1/2] Generating features...")
            feature_req = {
                "requirement_text": requirement,
                "project": project,
                "module": module
            }
            feature_response = requests.post(
                f"{self.base_url}/generate-features",
                json=feature_req,
                timeout=30
            )
            feature_data = feature_response.json()

            if feature_data.get("status") == "success":
                print(f"  [OK] Features generated")
                for feature_file in feature_data.get("features", []):
                    print(f"    File: {feature_file}")
                print("\n  Conventions applied:")
                for convention in feature_data.get("conventions", []):
                    print(f"    {convention}")
            else:
                print(f"  [ERROR] Failed: {feature_data}")
                return False

            # Generate pages
            print("\n[2/2] Generating page objects...")
            page_req = {
                "requirement_text": requirement,
                "project": project,
                "module": module
            }
            page_response = requests.post(
                f"{self.base_url}/generate-pages",
                json=page_req,
                timeout=30
            )
            page_data = page_response.json()

            if page_data.get("status") == "success":
                print(f"  [OK] Pages generated")
                for page_file in page_data.get("pages", []):
                    print(f"    File: {Path(page_file).name}")
                print("\n  Conventions applied:")
                for convention in page_data.get("conventions", []):
                    print(f"    {convention}")
            else:
                print(f"  [ERROR] Failed: {page_data}")
                return False

            print("\n" + "="*60)
            print("[OK] Test Generation Complete")
            print("="*60)
            print("\nNext steps:")
            print("  1. Run Maven: mvn clean verify")
            print("  2. View report: target/allure-report/index.html")

            return True

        except Exception as e:
            print(f"[ERROR] Error: {e}")
            return False

    def stop_service(self):
        """Stop RAG service"""
        if self.service_process:
            self.service_process.terminate()
            print("\n[OK] Service stopped")

def main():
    parser = argparse.ArgumentParser(
        description="RAG Orchestrator - Generate test artifacts using RAG service"
    )

    parser.add_argument(
        "command",
        choices=["start", "list", "generate", "stop"],
        help="Command to execute"
    )

    parser.add_argument(
        "-r", "--requirement",
        help="Requirement text for test generation"
    )

    parser.add_argument(
        "-p", "--project",
        default="automationexercise",
        help="Project name (automationexercise, saucedemo)"
    )

    parser.add_argument(
        "-m", "--module",
        help="Module name (optional, defaults to project name)"
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="RAG service host (default: 127.0.0.1)"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="RAG service port (default: 8080)"
    )

    args = parser.parse_args()

    orchestrator = RAGOrchestrator(args.host, args.port)

    if args.command == "start":
        orchestrator.start_service()

    elif args.command == "list":
        if not orchestrator.start_service():
            sys.exit(1)
        orchestrator.list_projects()

    elif args.command == "generate":
        if not args.requirement:
            print("✗ --requirement is required for generate command")
            sys.exit(1)

        if not orchestrator.start_service():
            sys.exit(1)

        success = orchestrator.generate_tests(
            args.requirement,
            args.project,
            args.module
        )
        sys.exit(0 if success else 1)

    elif args.command == "stop":
        orchestrator.stop_service()

if __name__ == "__main__":
    main()

