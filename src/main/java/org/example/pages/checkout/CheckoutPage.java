package org.example.pages.checkout;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * CheckoutPage: Page object for checkout module
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class CheckoutPage extends BasePage {

    // Locators - Public for generic step definitions
    public static final By FIRST_NAME = By.id("first-name");
    public static final By LAST_NAME = By.id("last-name");
    public static final By POSTAL_CODE = By.id("postal-code");
    public static final By CONTINUE_BUTTON = By.id("continue");
    public static final By CANCEL_BUTTON = By.id("cancel");
    public static final By ERROR_MESSAGE = By.cssSelector("[data-test='error']");
    public static final By CHECKOUT_INFO_TITLE = By.className("title");

    public CheckoutPage(WebDriver driver) {
        super(driver);
    }
}

