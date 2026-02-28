# Master Orchestrator - Complete Guide

## What is Master Orchestrator?

The Master Orchestrator is an **intelligent automation system** that monitors your `requirements.md` file and automatically:

1. **Monitors Requirements** - Detects changes in requirements.md
2. **Generates Features** - Creates Cucumber feature files from requirements (RAG-powered)
3. **Generates Page Objects** - Creates page objects by analyzing DOM (RAG-powered)
4. **Removes Duplicates** - Checks for duplicate steps and locators
5. **Runs Tests** - Executes Cucumber tests via Maven
6. **Analyzes Failures** - Uses RAG to understand why tests failed
7. **Generates Reports** - Creates Allure HTML reports

---

## Quick Start

### 1. Prerequisites
```bash
# Check Python 3.9+
python --version

# Check Maven 3.6+
mvn --version

# Check Java 11+
java -version

# Ollama running (for RAG)
ollama serve  # In separate terminal
```

### 2. Run Master Orchestrator (Full Flow)
```bash
cd D:\DreamProject\reflectioncucumber
python master_orchestrator.py
```

### 3. View Reports
```bash
# Allure report
mvn allure:serve
# Opens: http://localhost:8080

# Or open file directly
target/allure-report/index.html
```

---

## Command Reference

### Full Automation Flow
```bash
python master_orchestrator.py
```
Runs all phases: Generate → Run Tests → Analyze → Report

### Generate Only (Feature + Page Objects)
```bash
python master_orchestrator.py --only-gen
```
Monitors requirements.md, generates features and pages if changed

### Run Tests Only
```bash
python master_orchestrator.py --only-tests
```
Skips generation, runs tests directly

### Skip Generation (Tests Only)
```bash
python master_orchestrator.py --skip-gen
```
Uses existing features/pages, runs tests

### Skip Tests (Generation Only)
```bash
python master_orchestrator.py --skip-tests
```
Generates features/pages, skips test execution

---

## How It Works

### Step 1: Requirement Monitoring
```
requirements.md → Hash calculation → Compare with stored hash
  ├─ CHANGED? → Proceed to generation
  └─ UNCHANGED? → Skip generation, run tests
```

### Step 2: Feature Generation (RAG)
```
Requirement Title
  ├─ "User Login"
  └─ RAG generates:
      ├─ Feature file with scenarios
      ├─ Given/When/Then steps
      └─ Saved to: src/test/resources/features/
```

Example generated feature:
```gherkin
Feature: User Login
  As a user
  I want to log in with valid credentials
  
  Scenario: Successful login
    Given I am on login page
    When I enter username "standard_user"
    And I enter password "secret_sauce"
    And I click login button
    Then I should see inventory page
```

### Step 3: Page Object Generation (DOM + RAG)
```
URL (www.saucedemo.com)
  ├─ Browser analyzes DOM
  ├─ Extracts locators
  └─ RAG generates Java Page Object:
      ├─ @FindBy annotations
      ├─ Getter methods
      └─ Saved to: src/main/java/org/example/pages/
```

Example generated page object:
```java
public class LoginPage extends BasePage {
    @FindBy(id = "user-name")
    private WebElement usernameField;
    
    @FindBy(id = "password")
    private WebElement passwordField;
    
    @FindBy(id = "login-button")
    private WebElement loginButton;
    
    public void login(String username, String password) {
        usernameField.sendKeys(username);
        passwordField.sendKeys(password);
        loginButton.click();
    }
}
```

### Step 4: Duplication Removal
```
All Feature Files
  ├─ Scan for duplicate steps
  ├─ Scan for duplicate locators
  └─ Consolidate into common steps
```

### Step 5: Test Execution
```
mvn clean verify
  ├─ Parse feature files
  ├─ Execute step definitions
  ├─ Run Selenium WebDriver
  └─ Generate JSON results
```

### Step 6: Failure Analysis (RAG)
```
Failed Test Results
  ├─ Extract error messages
  ├─ Send to RAG
  └─ RAG suggests:
      ├─ Root cause (e.g., "Selector changed")
      ├─ Fix needed
      └─ Prevention strategy
```

### Step 7: Report Generation
```
Allure Report
  ├─ Parse JSON results
  ├─ Generate HTML dashboard
  ├─ Create charts & graphs
  └─ Deploy to GitHub Pages
```

---

## Configuration

### requirements.md Format
```markdown
## Feature Title

Description of the feature

- Acceptance Criteria 1
- Acceptance Criteria 2
- Acceptance Criteria 3
```

Example:
```markdown
## User Login

As a user, I want to log in with valid credentials so I can access inventory.

- User enters valid username
- User enters valid password
- System validates credentials
- User is redirected to inventory
```

### State File (.orchestrator_state.json)
Tracks:
- Last requirements hash (detects changes)
- Generated features
- Generated pages
- Test results
- Last execution time

---

## Integration with GitHub Actions

The master orchestrator runs automatically on every push:

```yaml
# .github/workflows/test-automation.yml
steps:
  - run: python master_orchestrator.py
    # Monitors requirements.md
    # Generates features if changed
    # Runs tests
    # Generates Allure report
```

---

## Troubleshooting

### Issue: RAG service not available
```
❌ RAG Service unavailable: Connection refused
```
**Solution:** Start Ollama
```bash
ollama serve
# In another terminal: ollama run mistral
```

### Issue: Feature generation failed
```
❌ Feature generation failed: [error]
```
**Solution:** Check RAG is running and config.yaml is correct

### Issue: Tests not running
```
❌ Tests FAILED (exit code: 1)
```
**Solution:** Check Maven pom.xml and test configuration

### Issue: No report generated
```
⚠️  Report generation issue
```
**Solution:**
```bash
# Check if allure-results exists
ls target/allure-results/

# Generate report manually
mvn allure:report
```

---

## Advanced Usage

### Run with Specific Tags
```bash
mvn test -Dcucumber.filter.tags="@smoke"
```

### Parallel Test Execution
```bash
mvn test -T 1C  # 1 thread per core
```

### Skip Report Deployment
Edit pom.xml to remove GitHub Pages step

### Use Different LLM
Edit `agent-service/config.yaml`:
```yaml
llm:
  provider: "openai"  # or "claude", "llama"
  model: "gpt-4"
  api_key: "${OPENAI_API_KEY}"
```

---

## Architecture Diagram

```
requirements.md (Updated)
        ↓
    Hash Check
        ↓
Changed? ──No──→ Use existing features
    │
   Yes
    ↓
Phase 1: Feature Generation (RAG)
    ├─ Parse requirements
    ├─ Call RAG/LLM
    └─ Generate .feature files
        ↓
Phase 2: Page Object Generation (DOM + RAG)
    ├─ Analyze DOM
    ├─ Extract locators
    └─ Generate Java classes
        ↓
Phase 3: Duplication Removal
    ├─ Check steps
    ├─ Check locators
    └─ Consolidate
        ↓
Phase 4: Test Execution (Maven)
    ├─ Run mvn verify
    ├─ Execute Cucumber
    └─ Generate results
        ↓
Phase 5: Failure Analysis (RAG)
    ├─ Parse failures
    ├─ Call RAG
    └─ Get suggestions
        ↓
Phase 6: Report Generation
    ├─ Generate Allure
    ├─ Upload artifacts
    └─ Deploy to GitHub Pages
        ↓
    COMPLETE ✅
```

---

## Monitoring & Logging

### Log Locations
```
master_orchestrator.log       - Main orchestrator log
target/surefire-reports/      - Maven test reports
target/allure-results/        - Allure JSON results
target/allure-report/         - Allure HTML report
.orchestrator_state.json      - Orchestrator state
```

### Checking Status
```bash
# View orchestrator log
tail -f master_orchestrator.log

# View test results
cat .orchestrator_state.json | jq .tests

# View generated files
ls -la src/test/resources/features/
ls -la src/main/java/org/example/pages/demo/
```

---

## Best Practices

1. **Update requirements.md regularly** - Orchestrator monitors changes
2. **Keep requirements clear** - Better quality features generated
3. **Review generated features** - Manually verify before running tests
4. **Fix test failures promptly** - RAG suggestions help diagnose
5. **Commit all generated files** - Version control your test code

---

## What's Next?

1. **Update requirements.md** with your test cases
2. **Run master_orchestrator.py** to generate tests
3. **Review generated features** in src/test/resources/features/
4. **Review generated pages** in src/main/java/org/example/pages/
5. **Commit changes** to GitHub
6. **Monitor Allure reports** on GitHub Pages

---

## Support

For issues:
- Check logs: `master_orchestrator.log`
- Check state: `.orchestrator_state.json`
- Verify RAG: `curl http://localhost:11434/api/tags`
- View reports: `mvn allure:serve`

---

**Master Orchestrator v1.0 - Agentic Test Automation with RAG Integration**

