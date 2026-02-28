package org.example.pages.intelligent_demo;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * LoginPage - Captured from: https://www.saucedemo.com
 * Real element locators discovered through intelligent page analysis
 */
public class LoginPage extends BasePage {
    // Username input field (ID-based locator - most reliable)
    public static final By USERNAME = By.id("user-name");

    // Password input field (ID-based locator)
    public static final By PASSWORD = By.id("password");

    // Login button (ID-based locator)
    public static final By LOGIN_BUTTON = By.id("login-button");

    // Error message container (CSS selector for error display)
    public static final By ERROR_MESSAGE = By.cssSelector("[data-test='error']");

    // Error text (alternate selector)
    public static final By ERROR_TEXT = By.cssSelector("h3[data-test='error']");

    // Username error hint
    public static final By USERNAME_ERROR = By.cssSelector("[data-test='username-error']");

    public LoginPage(WebDriver driver) {
        super(driver);
    }
}