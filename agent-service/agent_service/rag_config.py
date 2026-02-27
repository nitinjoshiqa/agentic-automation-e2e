"""
RAG Configuration - Plug and Play
All information needed for RAG service to work independently
"""

RAG_CONFIG = {
    "framework": {
        "root_path": "../../..",
        "locator_naming": "UPPER_SNAKE_CASE",
        "base_page_class": "org.example.base.BasePage",
    },

    "projects": {
        "automationexercise": {
            "name": "Automation Exercise",
            "site_url": "https://automationexercise.com",
            "module": "automationexercise",
            "package": "org.example.pages.automationexercise",
            "features_dir": "src/test/resources/features/automationexercise",
            "pages_dir": "src/main/java/org/example/pages/automationexercise",
            "pages": ["LoginPage", "SignupPage", "ProductsPage", "CartPage", "CheckoutPage"],
            "locators": {
                "LoginPage": {
                    "LOGIN_EMAIL": "input[data-qa='login-email']",
                    "LOGIN_PASSWORD": "input[data-qa='login-password']",
                    "LOGIN_BUTTON": "button[data-qa='login-button']",
                    "ERROR_MESSAGE": "p[data-qa='error-message']",
                    "SIGNUP_NAME": "input[data-qa='signup-name']",
                    "SIGNUP_EMAIL": "input[data-qa='signup-email']",
                    "SIGNUP_BUTTON": "button[data-qa='signup-button']",
                },
                "SignupPage": {
                    "SIGNUP_NAME": "input[data-qa='signup-name']",
                    "SIGNUP_EMAIL": "input[data-qa='signup-email']",
                    "PASSWORD": "input[data-qa='password']",
                    "FIRST_NAME": "input[data-qa='first_name']",
                    "LAST_NAME": "input[data-qa='last_name']",
                    "ADDRESS": "input[data-qa='address']",
                    "COUNTRY": "select[data-qa='country']",
                    "CREATE_ACCOUNT": "button[data-qa='create-account']",
                },
                "ProductsPage": {
                    "PRODUCT_LIST": "div.features_items",
                    "PRODUCT_ITEMS": "div.col-sm-4",
                    "PRODUCT_NAME": "p",
                    "ADD_TO_CART": "a[data-product-id]",
                    "SEARCH_INPUT": "input[id='search_product']",
                },
                "CartPage": {
                    "CART_ITEMS": "table tbody tr",
                    "ITEM_NAME": "a[href*='/product/']",
                    "REMOVE_ITEM": "a[class='cart_quantity_delete']",
                    "PROCEED_CHECKOUT": "a[href='/checkout']",
                },
                "CheckoutPage": {
                    "ADDRESS": "textarea[name='address']",
                    "COUNTRY": "select[name='country']",
                    "CARD_NAME": "input[data-qa='name-on-card']",
                    "PAY_BUTTON": "button[id='submit']",
                },
            }
        },

        "saucedemo": {
            "name": "Sauce Demo",
            "site_url": "https://www.saucedemo.com",
            "module": "saucedemo",
            "package": "org.example.pages.saucedemo",
            "features_dir": "src/test/resources/features/saucedemo",
            "pages_dir": "src/main/java/org/example/pages/saucedemo",
            "pages": ["LoginPage", "InventoryPage", "CartPage", "CheckoutPage"],
            "locators": {
                "LoginPage": {
                    "USERNAME": "input[id='user-name']",
                    "PASSWORD": "input[id='password']",
                    "LOGIN_BUTTON": "input[id='login-button']",
                    "ERROR_MESSAGE": "h3[data-test='error']",
                },
                "InventoryPage": {
                    "INVENTORY_CONTAINER": "div[id='inventory_container']",
                    "PRODUCT_ITEMS": "div.inventory_item",
                    "ADD_TO_CART": "button[data-test*='add-to-cart']",
                    "CART_BADGE": "span.shopping_cart_badge",
                },
                "CartPage": {
                    "CART_ITEMS": "div.cart_item",
                    "ITEM_NAME": "div.inventory_item_name",
                    "CHECKOUT_BUTTON": "button[id='checkout']",
                },
                "CheckoutPage": {
                    "FIRST_NAME": "input[data-test='firstName']",
                    "LAST_NAME": "input[data-test='lastName']",
                    "POSTAL_CODE": "input[data-test='postalCode']",
                    "FINISH_BUTTON": "button[id='finish']",
                },
            }
        },
    }
}

