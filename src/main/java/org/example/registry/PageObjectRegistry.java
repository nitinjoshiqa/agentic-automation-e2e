package org.example.registry;

import org.example.context.ScenarioContext;
import org.example.pages.cart.CartPage;
import org.example.pages.checkout.CheckoutPage;
import org.example.pages.checkout.CheckoutSummaryPage;
import org.example.pages.confirmation.ConfirmationPage;
import org.example.pages.inventory.InventoryPage;
import org.example.pages.login.LoginPage;

import java.util.HashMap;
import java.util.Map;

/**
 * PageObjectRegistry: Registry for all page objects
 * Enables dynamic page object retrieval by name
 * Supports reflection-based generic step definitions
 */
public class PageObjectRegistry {
    private final Map<String, Object> pageObjectMap;
    private final ScenarioContext scenarioContext;

    public PageObjectRegistry(ScenarioContext scenarioContext) {
        this.scenarioContext = scenarioContext;
        this.pageObjectMap = new HashMap<>();
        initializePageObjects();
    }

    /**
     * Initialize all page objects and register them
     */
    private void initializePageObjects() {
        registerPageObject("LoginPage", scenarioContext.getLoginPage());
        registerPageObject("InventoryPage", scenarioContext.getInventoryPage());
        registerPageObject("CartPage", scenarioContext.getCartPage());
        registerPageObject("CheckoutPage", scenarioContext.getCheckoutPage());
        registerPageObject("CheckoutSummaryPage", scenarioContext.getCheckoutSummaryPage());
        registerPageObject("ConfirmationPage", scenarioContext.getConfirmationPage());
    }

    /**
     * Register a page object
     */
    public void registerPageObject(String pageName, Object pageObject) {
        pageObjectMap.put(pageName, pageObject);
    }

    /**
     * Get page object by name
     */
    public Object getPageObject(String pageName) {
        if (!pageObjectMap.containsKey(pageName)) {
            throw new RuntimeException("Page object not found: " + pageName +
                                     ". Available: " + pageObjectMap.keySet());
        }
        return pageObjectMap.get(pageName);
    }

    /**
     * Check if page object exists
     */
    public boolean hasPageObject(String pageName) {
        return pageObjectMap.containsKey(pageName);
    }

    /**
     * Get all registered page objects
     */
    public Map<String, Object> getAllPageObjects() {
        return new HashMap<>(pageObjectMap);
    }

    /**
     * Get current scenario context
     */
    public ScenarioContext getScenarioContext() {
        return scenarioContext;
    }

    /**
     * Clear registry
     */
    public void clear() {
        pageObjectMap.clear();
    }
}

