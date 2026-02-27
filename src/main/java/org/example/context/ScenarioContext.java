package org.example.context;

import org.example.config.DriverManager;
import org.example.pages.cart.CartPage;
import org.example.pages.inventory.InventoryPage;
import org.example.pages.login.LoginPage;
import org.example.pages.checkout.CheckoutPage;
import org.example.pages.checkout.CheckoutSummaryPage;
import org.example.pages.confirmation.ConfirmationPage;
import org.openqa.selenium.WebDriver;

import java.lang.reflect.Constructor;

/**
 * ScenarioContext: Context class to hold shared data and page objects
 * Uses reflection to instantiate page objects dynamically
 */
public class ScenarioContext {
    private WebDriver driver;
    private LoginPage loginPage;
    private InventoryPage inventoryPage;
    private CartPage cartPage;
    private CheckoutPage checkoutPage;
    private CheckoutSummaryPage checkoutSummaryPage;
    private ConfirmationPage confirmationPage;

    public ScenarioContext() {
        this.driver = DriverManager.getInstance().initializeDriver();
        initializePageObjects();
    }

    /**
     * Initialize page objects using reflection
     */
    private void initializePageObjects() {
        this.loginPage = initializePageObject(LoginPage.class);
        this.inventoryPage = initializePageObject(InventoryPage.class);
        this.cartPage = initializePageObject(CartPage.class);
        this.checkoutPage = initializePageObject(CheckoutPage.class);
        this.checkoutSummaryPage = initializePageObject(CheckoutSummaryPage.class);
        this.confirmationPage = initializePageObject(ConfirmationPage.class);
    }

    /**
     * Dynamically instantiate page object using reflection
     */
    @SuppressWarnings("unchecked")
    private <T> T initializePageObject(Class<T> pageClass) {
        try {
            Constructor<T> constructor = pageClass.getDeclaredConstructor(WebDriver.class);
            return constructor.newInstance(driver);
        } catch (Exception e) {
            throw new RuntimeException("Failed to initialize page object: " + pageClass.getSimpleName(), e);
        }
    }

    /**
     * Get page object instance using reflection
     */
    public <T> T getPageObject(Class<T> pageClass) {
        try {
            if (pageClass == LoginPage.class) {
                return (T) loginPage;
            } else if (pageClass == InventoryPage.class) {
                return (T) inventoryPage;
            } else if (pageClass == CartPage.class) {
                return (T) cartPage;
            } else if (pageClass == CheckoutPage.class) {
                return (T) checkoutPage;
            } else if (pageClass == CheckoutSummaryPage.class) {
                return (T) checkoutSummaryPage;
            } else if (pageClass == ConfirmationPage.class) {
                return (T) confirmationPage;
            }
            return initializePageObject(pageClass);
        } catch (Exception e) {
            throw new RuntimeException("Page object not found: " + pageClass.getSimpleName(), e);
        }
    }

    // Getters for page objects
    public WebDriver getDriver() {
        return driver;
    }

    public LoginPage getLoginPage() {
        return loginPage;
    }

    public InventoryPage getInventoryPage() {
        return inventoryPage;
    }

    public CartPage getCartPage() {
        return cartPage;
    }

    public CheckoutPage getCheckoutPage() {
        return checkoutPage;
    }

    public CheckoutSummaryPage getCheckoutSummaryPage() {
        return checkoutSummaryPage;
    }

    public ConfirmationPage getConfirmationPage() {
        return confirmationPage;
    }

    /**
     * Clean up resources
     */
    public void cleanup() {
        DriverManager.getInstance().quitDriver();
    }
}

