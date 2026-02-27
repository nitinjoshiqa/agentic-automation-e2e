# End-to-End Agentic Flow - Quick Commands

## One-Command E2E Flow (PowerShell)

### For SauceDemo
```bash
cd D:\DreamProject\reflectioncucumber\agent-service
powershell -File .\Run-E2E-Demo.ps1 -Project saucedemo -Requirement "As a user I want to login and add items to cart"
```

### For AutomationExercise
```bash
powershell -File .\Run-E2E-Demo.ps1 -Project automationexercise -Requirement "As a user I want to register and browse products"
```

---

## Step-by-Step Approach

### Step 1: Start RAG Service
```bash
.venv\Scripts\python.exe rag_orchestrator.py start
```

### Step 2: Generate Features & Pages (from requirement only!)
```bash
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "As a user I want to login with valid credentials and add products to shopping cart" \
  -p saucedemo
```

### Step 3: Run Tests
```bash
cd ..
mvn clean verify
```

### Step 4: View Report
```bash
start target\allure-report\index.html
```

---

## What RAG Does Automatically

When you provide requirement:
```
"As a user I want to login and add products to cart"
```

RAG automatically:
1. **Detects Pages**
   - "login" → LoginPage ✓
   - "products" + "cart" → InventoryPage, CartPage ✓

2. **Generates Features** (Gherkin)
   ```gherkin
   Feature: User login and add products to cart
     Scenario: User successfully logs in
       When I enter "user" in "username" in "LoginPage"
       And I click "loginButton" on "LoginPage"
       Then "inventoryContainer" should be displayed on "InventoryPage"
   ```

3. **Generates Page Objects** (Java)
   ```java
   public class LoginPage extends BasePage {
       public static final By USERNAME = By.id("user-name");
       public static final By PASSWORD = By.id("password");
       public static final By LOGIN_BUTTON = By.id("login-button");
   }
   ```

4. **Runs Tests**
   - Maven compiles
   - Cucumber executes
   - Selenium automates

5. **Generates Report**
   - Allure dashboard
   - Charts and metrics
   - Opens in browser

---

## Different Requirement Examples

### Example 1: Login Flow
```bash
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "User should be able to login with valid credentials" \
  -p saucedemo
```
→ Detects: LoginPage, InventoryPage

### Example 2: Registration Flow
```bash
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "New user can register and create account" \
  -p automationexercise
```
→ Detects: SignupPage, LoginPage

### Example 3: Shopping Flow
```bash
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "User browses products, adds to cart and checks out" \
  -p saucedemo
```
→ Detects: InventoryPage, CartPage, CheckoutPage

### Example 4: Complete Flow
```bash
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "User registers, logs in, browses products, adds items to cart and completes checkout" \
  -p automationexercise
```
→ Detects: SignupPage, LoginPage, ProductsPage, CartPage, CheckoutPage

---

## List Available Projects
```bash
.venv\Scripts\python.exe rag_orchestrator.py list
```

Output:
```
Project: Automation Exercise
  Module: automationexercise
  Site: https://automationexercise.com
  Pages: LoginPage, SignupPage, ProductsPage, CartPage, CheckoutPage

Project: Sauce Demo
  Module: saucedemo
  Site: https://www.saucedemo.com
  Pages: LoginPage, InventoryPage, CartPage, CheckoutPage
```

---

## Full E2E Flow in One Terminal

### Terminal 1: Everything in Order
```bash
cd D:\DreamProject\reflectioncucumber\agent-service

# 1. Start service
.venv\Scripts\python.exe rag_orchestrator.py start

# 2. Generate features & pages (in new terminal)
.venv\Scripts\python.exe rag_orchestrator.py generate \
  -r "User login and add to cart" \
  -p saucedemo

# 3. Run tests
cd ..
mvn clean verify

# 4. View report
start target\allure-report\index.html
```

---

## Verify RAG is Working

### Check 1: Service Health
```bash
curl http://localhost:8080/health
```
Expected: `{"status":"ok","service":"context-aware-rag",...}`

### Check 2: Generated Files
```bash
# Features
type ..\src\test\resources\features\saucedemo\saucedemo_generated.feature

# Pages
type ..\src\main\java\org\example\pages\saucedemo\LoginPage.java
```

### Check 3: Generated Features Use Generic Steps
```gherkin
When I enter "X" in "field" in "PageName"
When I click "element" on "PageName"
Then "element" should be displayed on "PageName"
```

### Check 4: Generated Pages Have Real Locators
```java
public static final By USERNAME = By.id("user-name");
public static final By PASSWORD = By.id("password");
```

---

## Troubleshooting

### Port 8080 Already in Use
```bash
netstat -ano | findstr :8080
taskkill /PID <PID> /F
```

### Service Won't Start
```bash
# Kill Python processes
taskkill /F /IM python.exe

# Try again
.venv\Scripts\python.exe rag_orchestrator.py start
```

### Generation Fails
```bash
# Check service is running
curl http://localhost:8080/health

# Verify project exists
.venv\Scripts\python.exe rag_orchestrator.py list

# Check config
cd agent_service
.venv\Scripts\python.exe -c "from rag_config import RAG_CONFIG; print(list(RAG_CONFIG['projects'].keys()))"
```

---

## Summary

**Complete agentic flow from requirement text ONLY:**

```bash
Requirement: "User login and add to cart"
    ↓
.venv\Scripts\python.exe rag_orchestrator.py generate -r "..." -p saucedemo
    ↓
✓ Features generated (automatic)
✓ Pages generated with real locators (automatic)
✓ Tests run (mvn clean verify)
✓ Report generated (allure)
```

**Everything automated from requirement text!** 🚀🤖

