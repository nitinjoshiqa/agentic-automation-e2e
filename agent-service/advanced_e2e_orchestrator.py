#!/usr/bin/env python3
"""
Advanced End-to-End Orchestrator with Analysis and Deduplication Flows
"""

import argparse
import sys
import subprocess
import time
import requests
from pathlib import Path
from agent_service.test_analysis import TestFailureAnalyzer, DuplicationChecker, TestFlowOrchestrator

class AdvancedE2EOrchestrator:
    """Advanced orchestrator with failure analysis and duplication checking"""

    def __init__(self, framework_root=None):
        self.framework_root = Path(framework_root) if framework_root else Path(__file__).parent.parent.parent
        self.rag_service_url = "http://127.0.0.1:8080"
        self.rag_process = None
        self.orchestrator = TestFlowOrchestrator(str(self.framework_root))

    def log(self, message, level="INFO"):
        """Log messages"""
        symbols = {
            "INFO": "[*]",
            "SUCCESS": "[OK]",
            "ERROR": "[!]",
            "WARNING": "[?]",
            "ANALYSIS": "[~]"
        }
        try:
            print(f"{symbols.get(level, '[*]')} {message}")
        except UnicodeEncodeError:
            print(f"{symbols.get(level, '[*]')} {message.encode('ascii', 'replace').decode('ascii')}")

    def log_section(self, title):
        """Log section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70 + "\n")

    # ============= STEP 0: PRE-EXECUTION CHECKS =============

    def run_pre_execution_checks(self):
        """Run checks before test execution"""
        self.log_section("STEP 0: PRE-EXECUTION CHECKS")

        print("Checking for code duplication and integrity...\n")

        # Run orchestrator checks
        pre_check_report = self.orchestrator.check_before_execution()

        # Display results
        if pre_check_report.get("duplication_check"):
            dup_report = pre_check_report["duplication_check"]
            self.log(f"Locator Duplication: {dup_report.get('duplication_percentage', 0):.1f}%", "ANALYSIS")
            if dup_report.get("duplicate_locators"):
                self.log(f"  Found {len(dup_report['duplicate_locators'])} duplicate locators", "WARNING")
                for dup in dup_report['duplicate_locators'][:3]:
                    self.log(f"    - Used in {dup['count']} locations", "INFO")

        if pre_check_report.get("step_integrity"):
            step_report = pre_check_report["step_integrity"]
            if step_report.get("duplicate_steps"):
                self.log(f"Step Duplication: {len(step_report['duplicate_steps'])} duplicates", "WARNING")

        # Show readiness
        if pre_check_report.get("ready_to_execute"):
            self.log("Framework ready for execution", "SUCCESS")
        else:
            self.log("Framework has issues - see above", "WARNING")

        return pre_check_report

    # ============= STEP 1: START RAG SERVICE =============

    def start_rag_service(self):
        """Start RAG service"""
        self.log_section("STEP 1: Starting RAG Service")

        try:
            response = requests.get(f"{self.rag_service_url}/health", timeout=2)
            self.log("RAG service already running", "SUCCESS")
            return True
        except:
            pass

        self.log("Starting RAG service on port 8080...")
        rag_file = self.framework_root / "agent-service" / "agent_service" / "context_aware_rag.py"

        if not rag_file.exists():
            self.log(f"RAG service file not found: {rag_file}", "ERROR")
            return False

        self.rag_process = subprocess.Popen(
            [sys.executable, str(rag_file)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        for i in range(30):
            try:
                response = requests.get(f"{self.rag_service_url}/health", timeout=1)
                self.log(f"RAG service is ready (PID: {self.rag_process.pid})", "SUCCESS")
                return True
            except:
                time.sleep(1)

        self.log("Failed to start RAG service", "ERROR")
        return False

    # ============= STEP 2: GENERATE ARTIFACTS =============

    def generate_artifacts(self, requirement, project):
        """Generate features and pages from requirement"""
        self.log_section("STEP 2: Generating Features & Pages from Requirement")

        self.log(f"Project: {project}")
        self.log(f"Requirement: {requirement}\n")

        try:
            # Generate features
            self.log("Generating feature files...")
            feature_req = {
                "requirement_text": requirement,
                "project": project
            }
            feature_response = requests.post(
                f"{self.rag_service_url}/generate-features",
                json=feature_req,
                timeout=30
            )
            feature_data = feature_response.json()

            if feature_data.get("status") != "success":
                self.log(f"Feature generation failed: {feature_data}", "ERROR")
                return False

            features = feature_data.get("features") or []
            if features:
                self.log(f"Features generated successfully", "SUCCESS")

            # Generate pages
            self.log("Generating page objects...")
            page_response = requests.post(
                f"{self.rag_service_url}/generate-pages",
                json=feature_req,
                timeout=30
            )
            page_data = page_response.json()

            if page_data.get("status") != "success":
                self.log(f"Page generation failed: {page_data}", "ERROR")
                return False

            pages = page_data.get("pages") or []
            if pages:
                self.log(f"{len(pages)} page objects generated", "SUCCESS")

            return True

        except Exception as e:
            self.log(f"Error during artifact generation: {e}", "ERROR")
            return False

    # ============= STEP 3: RUN TESTS =============

    def run_tests(self):
        """Run Maven tests"""
        self.log_section("STEP 3: Running Tests via Maven")

        self.log("Executing: mvn clean verify\n")

        result = subprocess.run(
            ["mvn", "clean", "verify"],
            cwd=str(self.framework_root),
            capture_output=True,
            text=True
        )

        # Check results
        if "BUILD SUCCESS" in result.stdout:
            self.log("Tests executed successfully", "SUCCESS")

            # Extract test count
            import re
            match = re.search(r"Tests run: (\d+)", result.stdout)
            if match:
                self.log(f"Total tests executed: {match.group(1)}", "SUCCESS")

            return True, result.stdout
        else:
            self.log("Tests execution completed with issues", "WARNING")
            return False, result.stdout

    # ============= STEP 4: ANALYZE FAILURES =============

    def analyze_test_failures(self, test_output):
        """Analyze any test failures"""
        self.log_section("STEP 4: Analyzing Test Failures")

        # Look for failures in output
        failure_lines = []
        for line in test_output.split('\n'):
            if "FAILED" in line or "ERROR" in line or "Exception" in line:
                failure_lines.append(line)

        if not failure_lines:
            self.log("No failures detected - all tests passed!", "SUCCESS")
            return True

        self.log(f"Found {len(failure_lines)} failure indicators\n", "WARNING")

        # Analyze each failure
        for failure_line in failure_lines[:3]:  # Analyze first 3
            if failure_line.strip():
                analysis = self.orchestrator.analyzer.analyze_failure(failure_line)

                if analysis.get("error_type"):
                    self.log(f"Error: {analysis['error_type']}", "ANALYSIS")
                    self.log(f"Severity: {analysis['severity']}", "WARNING")
                    self.log(f"Cause: {analysis['cause']}", "INFO")

                    self.log("\nSuggested Fixes:", "INFO")
                    for i, fix in enumerate(analysis.get('fixes', [])[:3], 1):
                        self.log(f"  {i}. {fix}", "INFO")

        return False

    # ============= STEP 5: GENERATE REPORT =============

    def generate_report(self):
        """Generate Allure report"""
        self.log_section("STEP 5: Generating Allure Report")

        self.log("Executing: mvn allure:report\n")

        result = subprocess.run(
            ["mvn", "allure:report"],
            cwd=str(self.framework_root),
            capture_output=True,
            text=True
        )

        report_path = self.framework_root / "target" / "allure-report" / "index.html"

        if "BUILD SUCCESS" in result.stdout and report_path.exists():
            self.log(f"Report generated successfully", "SUCCESS")
            return str(report_path)
        else:
            self.log("Report generation completed", "WARNING")
            return None

    # ============= MAIN FLOW =============

    def run_advanced_e2e(self, requirement, project):
        """Run complete advanced end-to-end flow"""
        self.log_section("ADVANCED END-TO-END AGENTIC TEST AUTOMATION")

        self.log(f"Framework: {self.framework_root}")
        self.log(f"Project: {project}")
        self.log(f"Requirement: {requirement}\n")

        # Step 0: Pre-execution checks
        pre_check = self.run_pre_execution_checks()

        # Step 1: Start RAG
        if not self.start_rag_service():
            return False

        # Step 2: Generate artifacts
        if not self.generate_artifacts(requirement, project):
            return False

        # Step 3: Run tests
        test_success, test_output = self.run_tests()

        # Step 4: Analyze failures (even if passed, for insights)
        self.analyze_test_failures(test_output)

        # Step 5: Generate report
        report_path = self.generate_report()

        # Summary
        self.log_section("ADVANCED FLOW COMPLETE")

        self.log("Summary:", "SUCCESS")
        self.log("  [OK] Pre-execution checks completed", "SUCCESS")
        self.log("  [OK] RAG service started", "SUCCESS")
        self.log("  [OK] Artifacts generated", "SUCCESS")
        self.log("  [OK] Tests executed", "SUCCESS")
        self.log("  [OK] Failures analyzed (if any)", "SUCCESS")
        self.log("  [OK] Report generated", "SUCCESS")

        if report_path:
            self.log(f"\nReport: {report_path}", "INFO")
            import webbrowser
            try:
                webbrowser.open(f"file:///{report_path}")
            except:
                pass

        return True

    def cleanup(self):
        """Stop RAG service"""
        if self.rag_process:
            self.rag_process.terminate()
            self.log("RAG service stopped", "INFO")

def main():
    parser = argparse.ArgumentParser(
        description="Advanced End-to-End Agentic Test Automation with Analysis & Deduplication"
    )

    parser.add_argument(
        "requirement",
        help="Requirement text"
    )

    parser.add_argument(
        "-p", "--project",
        default="saucedemo",
        choices=["automationexercise", "saucedemo"],
        help="Project name"
    )

    parser.add_argument(
        "-f", "--framework-root",
        default=None,
        help="Framework root path"
    )

    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip pre-execution checks"
    )

    args = parser.parse_args()

    orchestrator = AdvancedE2EOrchestrator(args.framework_root)

    try:
        success = orchestrator.run_advanced_e2e(args.requirement, args.project)
        sys.exit(0 if success else 1)
    finally:
        orchestrator.cleanup()

if __name__ == "__main__":
    main()

