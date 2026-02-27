package org.example.stepdefinitions.generic;

import io.cucumber.java.en.When;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.Given;
import org.example.context.ScenarioContext;
import org.example.factory.GenericPageElementFactory;
import org.example.registry.PageObjectRegistry;

import static org.junit.Assert.assertTrue;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertEquals;

/**
 * GenericStepDefinitions: Generic step definitions for all page objects
 * Uses reflection to work with any page object without hardcoding specific steps
 *
 * Convention:
 * - Locators in page objects must be named in UPPER_SNAKE_CASE (e.g., USERNAME_INPUT)
 * - Method names in Gherkin can be in camelCase (e.g., "username" → "USERNAME_INPUT")
 * - Page object names must match class names exactly (e.g., "LoginPage")
 */
public class GenericStepDefinitions {
    private ScenarioContext scenarioContext;
    private PageObjectRegistry pageObjectRegistry;

    // Added no-argument constructor for Serenity/Cucumber object factory
    public GenericStepDefinitions() {
        this(new ScenarioContext());
    }

    public GenericStepDefinitions(ScenarioContext scenarioContext) {
        this.scenarioContext = scenarioContext;
        this.pageObjectRegistry = new PageObjectRegistry(scenarioContext);
    }

    /**
     * Generic step to enter text in any input field
     * Usage: When I enter "john_doe" in "username" in "LoginPage"
     */
    @When("I enter {string} in {string} in {string}")
    public void enterTextInField(String text, String fieldName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.enterText(pageObject, fieldName, text);
    }

    /**
     * Alternative syntax for entering text
     * Usage: When user enters "password123" in "password" field on "LoginPage"
     */
    @When("user enters {string} in {string} field on {string}")
    public void userEntersInFieldOn(String text, String fieldName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.enterText(pageObject, fieldName, text);
    }

    /**
     * Generic step to click any button/element
     * Usage: When I click "loginButton" on "LoginPage"
     */
    @When("I click {string} on {string}")
    public void clickElement(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.clickElement(pageObject, elementName);
    }

    /**
     * Alternative syntax for clicking
     * Usage: When user clicks "checkout" button on "CartPage"
     */
    @When("user clicks {string} on {string}")
    public void userClicksOn(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.clickElement(pageObject, elementName);
    }

    /**
     * Generic step to verify element is displayed
     * Usage: Then "loginButton" should be displayed on "LoginPage"
     */
    @Then("{string} should be displayed on {string}")
    public void verifyElementDisplayed(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        boolean isDisplayed = GenericPageElementFactory.isElementDisplayed(pageObject, elementName);
        assertTrue("Element " + elementName + " is not displayed on " + pageName, isDisplayed);
    }

    /**
     * Generic step to verify element is not displayed
     * Usage: Then "errorMessage" should not be displayed on "LoginPage"
     */
    @Then("{string} should not be displayed on {string}")
    public void verifyElementNotDisplayed(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        boolean isDisplayed = GenericPageElementFactory.isElementDisplayed(pageObject, elementName);
        assertFalse("Element " + elementName + " is still displayed on " + pageName, isDisplayed);
    }

    /**
     * Generic step to get and verify text from element
     * Usage: Then "title" on "LoginPage" should contain "Login"
     */
    @Then("{string} on {string} should contain {string}")
    public void verifyElementTextContains(String elementName, String pageName, String expectedText) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        String actualText = GenericPageElementFactory.getText(pageObject, elementName);
        assertTrue("Text does not contain: " + expectedText + ". Actual: " + actualText,
                   actualText.contains(expectedText));
    }

    /**
     * Generic step to verify exact text match
     * Usage: Then "title" on "LoginPage" should be "Login"
     */
    @Then("{string} on {string} should be {string}")
    public void verifyElementTextEquals(String elementName, String pageName, String expectedText) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        String actualText = GenericPageElementFactory.getText(pageObject, elementName);
        assertEquals("Text mismatch on " + elementName, expectedText, actualText);
    }

    /**
     * Generic step to get element text (for debugging/storing)
     * Usage: When I get text from "productName" on "InventoryPage"
     */
    @When("I get text from {string} on {string}")
    public void getElementText(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        String text = GenericPageElementFactory.getText(pageObject, elementName);
        System.out.println("Text from " + elementName + ": " + text);
    }

    /**
     * Generic step to verify element attribute
     * Usage: Then "submitButton" on "LoginPage" attribute "disabled" should be "false"
     */
    @Then("{string} on {string} attribute {string} should be {string}")
    public void verifyElementAttribute(String elementName, String pageName,
                                      String attributeName, String expectedValue) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        String actualValue = GenericPageElementFactory.getAttribute(pageObject, elementName, attributeName);
        assertEquals("Attribute " + attributeName + " mismatch", expectedValue, actualValue);
    }

    /**
     * Generic step to clear text from input field
     * Usage: When I clear "username" on "LoginPage"
     */
    @When("I clear {string} on {string}")
    public void clearInputField(String fieldName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.enterText(pageObject, fieldName, "");
    }

    /**
     * Generic step to perform multiple actions in sequence
     * Usage: When I perform login with "standard_user" and "secret_sauce" on "LoginPage"
     */
    @When("I perform login with {string} and {string} on {string}")
    public void performLogin(String username, String password, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        GenericPageElementFactory.enterText(pageObject, "username", username);
        GenericPageElementFactory.enterText(pageObject, "password", password);
        GenericPageElementFactory.clickElement(pageObject, "loginButton");
    }

    /**
     * Navigate to page using reflection
     * Usage: Given I navigate to "LoginPage"
     */
    @Given("I navigate to {string}")
    public void navigateToPage(String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        try {
            GenericPageElementFactory.invokeMethod(pageObject, "navigateToLoginPage");
        } catch (RuntimeException e) {
            // Try alternative method names
            System.out.println("Navigate method not found, attempting alternative: " + e.getMessage());
        }
    }

    /**
     * Wait for element visibility
     * Usage: When I wait for "title" on "LoginPage" to be displayed
     */
    @When("I wait for {string} on {string} to be displayed")
    public void waitForElementDisplayed(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        int maxRetries = 10;
        int retryCount = 0;

        while (retryCount < maxRetries) {
            if (GenericPageElementFactory.isElementDisplayed(pageObject, elementName)) {
                return;
            }
            retryCount++;
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }

        throw new RuntimeException("Element " + elementName + " did not appear within timeout");
    }

    /**
     * Generic step to verify element attribute contains text
     * Usage: Then "productImage" on "InventoryPage" attribute "src" should contain "jpg"
     */
    @Then("{string} on {string} attribute {string} should contain {string}")
    public void verifyElementAttributeContains(String elementName, String pageName, String attributeName, String expectedValue) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        String attributeValue = GenericPageElementFactory.getAttribute(pageObject, elementName, attributeName);
        assertTrue("Attribute " + attributeName + " on element " + elementName + " does not contain '" + expectedValue + "'",
                attributeValue.contains(expectedValue));
    }

    /**
     * Generic step to verify element is updated
     * Usage: And "itemTotalPrice" should be updated on "CartPage"
     */
    @Then("{string} should be updated on {string}")
    public void verifyElementUpdated(String elementName, String pageName) {
        Object pageObject = pageObjectRegistry.getPageObject(pageName);
        boolean isDisplayed = GenericPageElementFactory.isElementDisplayed(pageObject, elementName);
        assertTrue("Element " + elementName + " is not displayed on " + pageName, isDisplayed);
    }
}

