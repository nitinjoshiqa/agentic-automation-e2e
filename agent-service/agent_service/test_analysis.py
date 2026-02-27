#!/usr/bin/env python3
"""
Test Failure Analyzer - Intelligent diagnosis and fixing
"""

import re
from typing import List, Dict, Any, Tuple

class TestFailureAnalyzer:
    """Analyzes test failures and suggests fixes"""

    def __init__(self):
        self.failure_patterns = {
            "NoSuchElementException": {
                "cause": "Locator not found on page",
                "fixes": [
                    "Verify locator selector is correct",
                    "Check if element exists in current page context",
                    "Update locator in page object",
                    "Add wait condition for element to appear",
                    "Verify page has loaded completely",
                ]
            },
            "StaleElementReferenceException": {
                "cause": "Element went stale (DOM refreshed)",
                "fixes": [
                    "Add wait for element after action",
                    "Re-find element before interaction",
                    "Use explicit waits instead of implicit",
                    "Add try-catch with re-find logic",
                ]
            },
            "TimeoutException": {
                "cause": "Action took too long",
                "fixes": [
                    "Increase timeout value",
                    "Wait for element visibility instead of presence",
                    "Check if element is clickable",
                    "Verify page load is complete",
                    "Check for loading spinners",
                ]
            },
            "AssertionError": {
                "cause": "Expected value doesn't match actual",
                "fixes": [
                    "Update expected value in test",
                    "Check if element has correct content",
                    "Verify test data is correct",
                    "Add print statements to debug values",
                    "Check for dynamic content changes",
                ]
            },
            "ElementNotInteractableException": {
                "cause": "Element exists but cannot be clicked/typed",
                "fixes": [
                    "Scroll element into view",
                    "Wait for element to be clickable",
                    "Check if element is covered by another",
                    "Add explicit wait for element readiness",
                    "Use JavaScript executor to click if needed",
                ]
            },
            "InvalidElementStateException": {
                "cause": "Element is disabled or read-only",
                "fixes": [
                    "Check if element is enabled",
                    "Wait for element to be enabled",
                    "Verify element is not disabled",
                    "Check form validation state",
                ]
            },
        }

    def analyze_failure(self, error_message: str) -> Dict[str, Any]:
        """Analyze test failure and suggest fixes"""

        analysis = {
            "error_type": None,
            "cause": None,
            "fixes": [],
            "severity": "LOW",
            "recommended_actions": []
        }

        # Match error type
        for error_type, details in self.failure_patterns.items():
            if error_type in error_message:
                analysis["error_type"] = error_type
                analysis["cause"] = details["cause"]
                analysis["fixes"] = details["fixes"]
                break

        # Determine severity
        if "NoSuchElementException" in error_message:
            analysis["severity"] = "CRITICAL"
        elif "TimeoutException" in error_message:
            analysis["severity"] = "HIGH"
        elif "AssertionError" in error_message:
            analysis["severity"] = "MEDIUM"
        else:
            analysis["severity"] = "LOW"

        # Recommended actions
        if analysis["severity"] == "CRITICAL":
            analysis["recommended_actions"] = [
                "1. Verify locators are correct and up-to-date",
                "2. Check if page structure has changed",
                "3. Update page object with new locators",
                "4. Re-run test to verify fix"
            ]
        elif analysis["severity"] == "HIGH":
            analysis["recommended_actions"] = [
                "1. Increase timeout values",
                "2. Add explicit waits",
                "3. Check page load completeness",
                "4. Monitor for external delays"
            ]

        return analysis

    def suggest_fix_code(self, error_type: str, element_name: str) -> str:
        """Generate fix code for common issues"""

        fixes = {
            "NoSuchElementException": f"""
# Fix: Add explicit wait for element
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "{element_name}"))
)
element = driver.find_element(By.ID, "{element_name}")
""",
            "StaleElementReferenceException": f"""
# Fix: Re-find element before use
try:
    element = driver.find_element(By.ID, "{element_name}")
    element.click()
except StaleElementReferenceException:
    # Re-find and retry
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "{element_name}"))
    )
    element = driver.find_element(By.ID, "{element_name}")
    element.click()
""",
            "TimeoutException": f"""
# Fix: Increase timeout and wait for clickability
element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.ID, "{element_name}"))
)
element.click()
""",
            "ElementNotInteractableException": f"""
# Fix: Scroll into view and wait for clickability
element = driver.find_element(By.ID, "{element_name}")
driver.execute_script("arguments[0].scrollIntoView(true);", element)
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "{element_name}"))
)
element.click()
"""
        }

        return fixes.get(error_type, "# Unable to suggest specific fix. See analyzer output.")


class DuplicationChecker:
    """Checks for code duplication in test framework"""

    def __init__(self, project_root: str):
        self.project_root = project_root
        self.duplicates_found = []

    def check_step_duplication(self, step_files: List[str]) -> Dict[str, Any]:
        """Check for duplicate step definitions"""

        report = {
            "total_steps": 0,
            "duplicate_steps": [],
            "files_affected": set(),
            "duplication_percentage": 0.0
        }

        step_patterns = {}

        for file_path in step_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Find @When, @Then, @Given patterns
                    patterns = re.findall(r'@(When|Then|Given)\("([^"]+)"\)', content)

                    for pattern_type, pattern_text in patterns:
                        report["total_steps"] += 1

                        key = pattern_text.lower()
                        if key not in step_patterns:
                            step_patterns[key] = []

                        step_patterns[key].append({
                            "file": file_path,
                            "pattern": pattern_text,
                            "type": pattern_type
                        })
                        report["files_affected"].add(file_path)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        # Find duplicates
        for pattern, occurrences in step_patterns.items():
            if len(occurrences) > 1:
                report["duplicate_steps"].append({
                    "pattern": pattern,
                    "count": len(occurrences),
                    "files": [o["file"] for o in occurrences]
                })

        # Calculate percentage
        if report["total_steps"] > 0:
            report["duplication_percentage"] = (
                len(report["duplicate_steps"]) / report["total_steps"]
            ) * 100

        return report

    def check_page_object_duplication(self, page_files: List[str]) -> Dict[str, Any]:
        """Check for duplicate locators across page objects"""

        report = {
            "total_locators": 0,
            "duplicate_locators": [],
            "pages_affected": set(),
            "duplication_percentage": 0.0
        }

        locator_map = {}

        for file_path in page_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Find locator patterns
                    locators = re.findall(
                        r'public static final By (\w+) = By\.([^;]+);',
                        content
                    )

                    for locator_name, locator_value in locators:
                        report["total_locators"] += 1

                        # Normalize value for comparison
                        normalized = locator_value.strip().lower()

                        if normalized not in locator_map:
                            locator_map[normalized] = []

                        locator_map[normalized].append({
                            "file": file_path,
                            "name": locator_name,
                            "value": locator_value
                        })
                        report["pages_affected"].add(file_path)

            except Exception as e:
                print(f"Error reading {file_path}: {e}")

        # Find duplicates
        for locator_value, occurrences in locator_map.items():
            if len(occurrences) > 1:
                report["duplicate_locators"].append({
                    "value": locator_value,
                    "count": len(occurrences),
                    "locations": [
                        f"{o['file']}::{o['name']}" for o in occurrences
                    ]
                })

        # Calculate percentage
        if report["total_locators"] > 0:
            report["duplication_percentage"] = (
                len(report["duplicate_locators"]) / report["total_locators"]
            ) * 100

        return report

    def generate_deduplication_suggestions(self, duplication_report: Dict) -> List[str]:
        """Generate suggestions to reduce duplication"""

        suggestions = []

        if duplication_report.get("duplicate_steps"):
            suggestions.append("=== STEP DEDUPLICATION SUGGESTIONS ===")
            suggestions.append(f"Found {len(duplication_report['duplicate_steps'])} duplicate step definitions")
            suggestions.append("\nOptions:")
            suggestions.append("1. Create shared step definition file")
            suggestions.append("2. Use inheritance for similar steps")
            suggestions.append("3. Create parameterized generic steps")
            suggestions.append("4. Remove redundant step files")

        if duplication_report.get("duplicate_locators"):
            suggestions.append("\n=== LOCATOR DEDUPLICATION SUGGESTIONS ===")
            suggestions.append(f"Found {len(duplication_report['duplicate_locators'])} duplicate locators")
            suggestions.append("\nOptions:")
            suggestions.append("1. Create shared locator constants file")
            suggestions.append("2. Use inheritance in page objects")
            suggestions.append("3. Create base page with common locators")
            suggestions.append("4. Use composition for shared elements")

        if duplication_report.get("duplication_percentage", 0) > 20:
            suggestions.append("\n⚠️  HIGH DUPLICATION: > 20%")
            suggestions.append("Recommend refactoring to reduce maintenance burden")

        return suggestions


class TestFlowOrchestrator:
    """Orchestrates complete test flow with analysis and deduplication checks"""

    def __init__(self, framework_root: str):
        self.framework_root = framework_root
        self.analyzer = TestFailureAnalyzer()
        self.dedup_checker = DuplicationChecker(framework_root)

    def check_before_execution(self) -> Dict[str, Any]:
        """Check for issues before executing tests"""

        pre_check_report = {
            "timestamp": self._get_timestamp(),
            "duplication_check": None,
            "locator_integrity": None,
            "step_integrity": None,
            "ready_to_execute": True,
            "issues": []
        }

        # Check duplication
        print("\n[*] Checking for code duplication...")
        page_files = self._find_page_files()
        step_files = self._find_step_files()

        if page_files:
            dup_locators = self.dedup_checker.check_page_object_duplication(page_files)
            pre_check_report["duplication_check"] = dup_locators

            if dup_locators.get("duplicate_locators"):
                pre_check_report["ready_to_execute"] = False
                pre_check_report["issues"].append(
                    f"Duplicate locators found: {len(dup_locators['duplicate_locators'])}"
                )
                print(f"[!] WARNING: {len(dup_locators['duplicate_locators'])} duplicate locators")

        if step_files:
            dup_steps = self.dedup_checker.check_step_duplication(step_files)
            pre_check_report["step_integrity"] = dup_steps

            if dup_steps.get("duplicate_steps"):
                pre_check_report["issues"].append(
                    f"Duplicate steps found: {len(dup_steps['duplicate_steps'])}"
                )
                print(f"[!] WARNING: {len(dup_steps['duplicate_steps'])} duplicate steps")

        return pre_check_report

    def analyze_test_failure(self, error_log: str) -> Dict[str, Any]:
        """Analyze test failure from log"""

        analysis = self.analyzer.analyze_failure(error_log)

        print("\n" + "="*60)
        print("TEST FAILURE ANALYSIS")
        print("="*60)
        print(f"\nError Type: {analysis['error_type']}")
        print(f"Severity: {analysis['severity']}")
        print(f"Cause: {analysis['cause']}")
        print("\nSuggested Fixes:")
        for i, fix in enumerate(analysis['fixes'], 1):
            print(f"  {i}. {fix}")

        if analysis['recommended_actions']:
            print("\nRecommended Actions:")
            for action in analysis['recommended_actions']:
                print(f"  {action}")

        return analysis

    def _find_page_files(self) -> List[str]:
        """Find all page object files"""
        from pathlib import Path

        try:
            pages_dir = Path(self.framework_root) / "src" / "main" / "java" / "org" / "example" / "pages"
            if pages_dir.exists():
                return [str(f) for f in pages_dir.rglob("*.java") if "Page" in f.name]
        except:
            pass

        return []

    def _find_step_files(self) -> List[str]:
        """Find all step definition files"""
        from pathlib import Path

        try:
            steps_dir = Path(self.framework_root) / "src" / "test" / "java" / "org" / "example" / "stepdefinitions"
            if steps_dir.exists():
                return [str(f) for f in steps_dir.rglob("*Steps.java")]
        except:
            pass

        return []

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

