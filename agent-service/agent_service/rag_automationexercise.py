#!/usr/bin/env python3
"""
Enhanced RAG Service - Specialized for automationexercise.com
Generates intelligent features and page objects for e-commerce automation
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path

app = FastAPI(title="Agentic RAG - Automation Exercise")

# ============= DATA MODELS =============

class FeatureRequest(BaseModel):
    requirement_text: str
    module: str = "automationexercise"
    site_url: str = "https://automationexercise.com"

class PageHint(BaseModel):
    page: str
    elements: Optional[List[str]] = []

class PageRequest(BaseModel):
    page_hints: List[PageHint]
    module: str = "automationexercise"
    site_url: str = "https://automationexercise.com"

class GenerationResponse(BaseModel):
    status: str
    mode: str
    features: Optional[List[str]] = None
    pages: Optional[List[str]] = None
    page_hints: Optional[List[dict]] = None

# ============= AUTOMATIONEXERCISE.COM SPECIFIC DATA =============

# Real locators from automationexercise.com
AUTOMATIONEXERCISE_LOCATORS = {
    "HomePage": {
        "signup_button": "a[href='/login']",
        "products_link": "a[href='/products']",
        "login_button": "a[href='/login']",
        "contact_us": "a[href='#contact-us']",
        "test_cases_link": "a[href='/test_cases']",
    },
    "SignupPage": {
        "signup_name": "input[data-qa='signup-name']",
        "signup_email": "input[data-qa='signup-email']",
        "signup_button": "button[data-qa='signup-button']",
        "title_label": "label[for='id_gender']",
        "password": "input[data-qa='password']",
        "day_select": "select[data-qa='days']",
        "month_select": "select[data-qa='months']",
        "year_select": "select[data-qa='years']",
        "first_name": "input[data-qa='first_name']",
        "last_name": "input[data-qa='last_name']",
        "address": "input[data-qa='address']",
        "country_select": "select[data-qa='country']",
        "state": "input[data-qa='state']",
        "city": "input[data-qa='city']",
        "zipcode": "input[data-qa='zipcode']",
        "mobile_number": "input[data-qa='mobile_number']",
        "create_account_button": "button[data-qa='create-account']",
        "success_message": "p[data-qa='account-created']",
    },
    "LoginPage": {
        "login_email": "input[data-qa='login-email']",
        "login_password": "input[data-qa='login-password']",
        "login_button": "button[data-qa='login-button']",
        "error_message": "p[data-qa='error-message']",
        "signup_email": "input[data-qa='signup-email']",
        "signup_name": "input[data-qa='signup-name']",
    },
    "ProductsPage": {
        "product_list": "div.features_items",
        "product_item": "div.col-sm-4",
        "product_name": "p[text()]",
        "product_price": "h2",
        "add_to_cart": "a[data-product-id]",
        "view_product": "a[href*='/product/']",
        "search_input": "input[id='search_product']",
        "search_button": "button[id='submit_search']",
        "category_list": "div.panel-group",
        "category_item": "a[data-toggle='collapse']",
        "brand_list": "div.brands_products",
    },
    "ProductDetailPage": {
        "product_image": "div.view-product img",
        "product_name": "h2",
        "product_price": "span[text()='Rs.']",
        "product_rating": "p.rating",
        "product_description": "p[text()]",
        "quantity_input": "input[id='quantity']",
        "add_to_cart_button": "button[class='btn']",
        "related_items": "div.recommended_items",
    },
    "CartPage": {
        "cart_items": "table tbody tr",
        "item_name": "a[href*='/product/']",
        "item_price": "td:nth-child(3)",
        "item_quantity": "button.cart_quantity_up",
        "item_total": "td:nth-child(5)",
        "remove_item": "a[class='cart_quantity_delete']",
        "cart_total": "tbody tr:last-child",
        "proceed_checkout": "a[href='/checkout']",
        "continue_shopping": "a[href='/products']",
    },
    "CheckoutPage": {
        "address": "textarea[name='address']",
        "country": "select[name='country']",
        "state": "input[name='state']",
        "city": "input[name='city']",
        "zipcode": "input[name='zipcode']",
        "mobile": "input[name='mobile_number']",
        "payment_desc": "textarea[name='payment_description']",
        "card_name": "input[data-qa='name-on-card']",
        "card_number": "input[data-qa='card-number']",
        "card_cvv": "input[data-qa='cvc']",
        "card_expire_month": "input[data-qa='expiry-month']",
        "card_expire_year": "input[data-qa='expiry-year']",
        "pay_button": "button[id='submit']",
    },
}

# ============= INTELLIGENT GENERATORS =============

def analyze_requirement_automationexercise(requirement: str) -> tuple[str, List[PageHint]]:
    """Analyze requirement and determine pages needed for automationexercise.com"""

    req_lower = requirement.lower()
    pages = []

    # Home page always included
    pages.append(PageHint(page="HomePage", elements=list(AUTOMATIONEXERCISE_LOCATORS["HomePage"].keys())))

    # Determine pages based on requirement
    if "signup" in req_lower or "register" in req_lower:
        pages.append(PageHint(page="SignupPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["SignupPage"].keys())))

    if "login" in req_lower or "authenticate" in req_lower:
        pages.append(PageHint(page="LoginPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["LoginPage"].keys())))

    if "product" in req_lower or "browse" in req_lower or "search" in req_lower:
        pages.append(PageHint(page="ProductsPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["ProductsPage"].keys())))
        pages.append(PageHint(page="ProductDetailPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["ProductDetailPage"].keys())))

    if "cart" in req_lower or "add to cart" in req_lower:
        pages.append(PageHint(page="CartPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["CartPage"].keys())))

    if "checkout" in req_lower or "order" in req_lower or "payment" in req_lower:
        pages.append(PageHint(page="CheckoutPage", elements=list(AUTOMATIONEXERCISE_LOCATORS["CheckoutPage"].keys())))

    # Generate intelligent features
    feature_content = f'''Feature: {requirement}

  Scenario: User completes main task successfully
    Given the user is on the automation exercise website
    When the user performs the required action
    Then the action completes successfully
    And the system confirms the action

  Scenario: User validates important fields
    Given the system is ready
    When the user interacts with required fields
    Then all fields are properly validated
    And appropriate messages are displayed
'''

    # Save feature file
    repo_root = Path(__file__).parent.parent.parent
    feature_dir = repo_root / "src" / "test" / "resources" / "features" / "automationexercise"
    feature_dir.mkdir(parents=True, exist_ok=True)

    feature_file = feature_dir / "AutomationExerciseFeatures.feature"
    feature_file.write_text(feature_content, encoding="utf-8")

    return str(feature_file), pages

def generate_pages_automationexercise(page_hints: List[PageHint], module: str) -> List[str]:
    """Generate Java page objects with real automationexercise.com locators"""

    repo_root = Path(__file__).parent.parent.parent
    page_dir = repo_root / "src" / "main" / "java" / "org" / "example" / "pages" / module
    page_dir.mkdir(parents=True, exist_ok=True)

    generated_files = []

    page_templates = {
        "HomePage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class HomePage extends BasePage {{
    public static final By SIGNUP_BUTTON = By.cssSelector("a[href='/login']");
    public static final By PRODUCTS_LINK = By.cssSelector("a[href='/products']");
    public static final By LOGIN_BUTTON = By.cssSelector("a[href='/login']");
    public static final By CONTACT_US = By.cssSelector("a[href='#contact-us']");
    
    public HomePage(WebDriver driver) {{
        super(driver);
    }}
}}''',

        "SignupPage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class SignupPage extends BasePage {{
    public static final By SIGNUP_NAME = By.cssSelector("input[data-qa='signup-name']");
    public static final By SIGNUP_EMAIL = By.cssSelector("input[data-qa='signup-email']");
    public static final By SIGNUP_BUTTON = By.cssSelector("button[data-qa='signup-button']");
    public static final By PASSWORD = By.cssSelector("input[data-qa='password']");
    public static final By FIRST_NAME = By.cssSelector("input[data-qa='first_name']");
    public static final By LAST_NAME = By.cssSelector("input[data-qa='last_name']");
    public static final By ADDRESS = By.cssSelector("input[data-qa='address']");
    public static final By COUNTRY = By.cssSelector("select[data-qa='country']");
    public static final By STATE = By.cssSelector("input[data-qa='state']");
    public static final By CITY = By.cssSelector("input[data-qa='city']");
    public static final By ZIPCODE = By.cssSelector("input[data-qa='zipcode']");
    public static final By MOBILE_NUMBER = By.cssSelector("input[data-qa='mobile_number']");
    public static final By CREATE_ACCOUNT = By.cssSelector("button[data-qa='create-account']");
    public static final By SUCCESS_MESSAGE = By.cssSelector("p[data-qa='account-created']");
    
    public SignupPage(WebDriver driver) {{
        super(driver);
    }}
}}''',

        "LoginPage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage extends BasePage {{
    public static final By LOGIN_EMAIL = By.cssSelector("input[data-qa='login-email']");
    public static final By LOGIN_PASSWORD = By.cssSelector("input[data-qa='login-password']");
    public static final By LOGIN_BUTTON = By.cssSelector("button[data-qa='login-button']");
    public static final By ERROR_MESSAGE = By.cssSelector("p[data-qa='error-message']");
    public static final By SIGNUP_EMAIL = By.cssSelector("input[data-qa='signup-email']");
    public static final By SIGNUP_NAME = By.cssSelector("input[data-qa='signup-name']");
    
    public LoginPage(WebDriver driver) {{
        super(driver);
    }}
}}''',

        "ProductsPage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class ProductsPage extends BasePage {{
    public static final By PRODUCT_LIST = By.cssSelector("div.features_items");
    public static final By PRODUCT_ITEMS = By.cssSelector("div.col-sm-4");
    public static final By PRODUCT_NAME = By.cssSelector("p");
    public static final By PRODUCT_PRICE = By.cssSelector("h2");
    public static final By ADD_TO_CART = By.cssSelector("a[data-product-id]");
    public static final By VIEW_PRODUCT = By.cssSelector("a[href*='/product/']");
    public static final By SEARCH_INPUT = By.cssSelector("input[id='search_product']");
    public static final By SEARCH_BUTTON = By.cssSelector("button[id='submit_search']");
    
    public ProductsPage(WebDriver driver) {{
        super(driver);
    }}
}}''',

        "CartPage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CartPage extends BasePage {{
    public static final By CART_ITEMS = By.cssSelector("table tbody tr");
    public static final By ITEM_NAME = By.cssSelector("a[href*='/product/']");
    public static final By ITEM_PRICE = By.cssSelector("td:nth-child(3)");
    public static final By ITEM_QUANTITY = By.cssSelector("button.cart_quantity_up");
    public static final By REMOVE_ITEM = By.cssSelector("a[class='cart_quantity_delete']");
    public static final By CART_TOTAL = By.cssSelector("tbody tr:last-child");
    public static final By PROCEED_CHECKOUT = By.cssSelector("a[href='/checkout']");
    public static final By CONTINUE_SHOPPING = By.cssSelector("a[href='/products']");
    
    public CartPage(WebDriver driver) {{
        super(driver);
    }}
}}''',

        "CheckoutPage": '''package org.example.pages.{module};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class CheckoutPage extends BasePage {{
    public static final By ADDRESS = By.cssSelector("textarea[name='address']");
    public static final By COUNTRY = By.cssSelector("select[name='country']");
    public static final By STATE = By.cssSelector("input[name='state']");
    public static final By CITY = By.cssSelector("input[name='city']");
    public static final By ZIPCODE = By.cssSelector("input[name='zipcode']");
    public static final By MOBILE = By.cssSelector("input[name='mobile_number']");
    public static final By CARD_NAME = By.cssSelector("input[data-qa='name-on-card']");
    public static final By CARD_NUMBER = By.cssSelector("input[data-qa='card-number']");
    public static final By CARD_CVV = By.cssSelector("input[data-qa='cvc']");
    public static final By CARD_EXPIRE_MONTH = By.cssSelector("input[data-qa='expiry-month']");
    public static final By CARD_EXPIRE_YEAR = By.cssSelector("input[data-qa='expiry-year']");
    public static final By PAY_BUTTON = By.cssSelector("button[id='submit']");
    
    public CheckoutPage(WebDriver driver) {{
        super(driver);
    }}
}}''',
    }

    # Generate for each hinted page
    for hint in page_hints:
        page_name = hint.page
        if page_name in page_templates:
            content = page_templates[page_name].format(module=module)
            page_file = page_dir / f"{page_name}.java"
            page_file.write_text(content, encoding="utf-8")
            generated_files.append(str(page_file))

    return generated_files

# ============= ENDPOINTS =============

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "service": "automation-exercise-rag"}

@app.post("/generate-features", response_model=GenerationResponse)
async def generate_features(request: FeatureRequest):
    """Generate features for automationexercise.com"""
    try:
        feature_file, page_hints = analyze_requirement_automationexercise(request.requirement_text)

        return GenerationResponse(
            status="success",
            mode="intelligent-automationexercise",
            features=[feature_file],
            page_hints=[hint.dict() for hint in page_hints]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-pages", response_model=GenerationResponse)
async def generate_pages(request: PageRequest):
    """Generate page objects with real automationexercise.com locators"""
    try:
        pages = generate_pages_automationexercise(request.page_hints, request.module)

        return GenerationResponse(
            status="success",
            mode="intelligent-automationexercise",
            pages=pages
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)

