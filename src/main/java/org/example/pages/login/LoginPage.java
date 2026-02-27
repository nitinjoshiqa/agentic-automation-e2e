package org.example.pages.login;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * LoginPage: Page object for login module
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class LoginPage extends BasePage {
    private static final String BASE_URL = "https://www.saucedemo.com/";

    // Locators - Public for generic step definitions
    public static final By USERNAME = By.id("user-name");
    public static final By PASSWORD = By.id("password");
    public static final By LOGIN_BUTTON = By.id("login-button");
    public static final By ERROR_MESSAGE = By.cssSelector("[data-test='error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }

    /**
     * Navigate to login page
     */
    public void navigateToLoginPage() {
        navigateTo(BASE_URL);
    }
}

