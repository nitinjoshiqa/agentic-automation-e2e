package org.example.base;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * BasePage: Base class for all page objects
 * Provides common methods for element interactions and waits
 */
public class BasePage {
    protected WebDriver driver;
    protected WebDriverWait wait;
    private static final Duration EXPLICIT_WAIT = Duration.ofSeconds(10);

    public BasePage(WebDriver driver) {
        this.driver = driver;
        this.wait = new WebDriverWait(driver, EXPLICIT_WAIT);
    }

    /**
     * Wait for element to be visible
     */
    public WebElement waitForElementVisibility(By locator) {
        return wait.until(ExpectedConditions.visibilityOfElementLocated(locator));
    }

    /**
     * Wait for element to be clickable
     */
    public WebElement waitForElementClickable(By locator) {
        return wait.until(ExpectedConditions.elementToBeClickable(locator));
    }

    /**
     * Click on element
     */
    public void click(By locator) {
        waitForElementClickable(locator).click();
    }

    /**
     * Send keys to element
     */
    public void sendKeys(By locator, String text) {
        WebElement element = waitForElementVisibility(locator);
        element.clear();
        element.sendKeys(text);
    }

    /**
     * Get text from element
     */
    public String getText(By locator) {
        return waitForElementVisibility(locator).getText();
    }

    /**
     * Check if element is displayed
     */
    public boolean isElementDisplayed(By locator) {
        try {
            return driver.findElement(locator).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Navigate to URL
     */
    public void navigateTo(String url) {
        driver.navigate().to(url);
    }

    /**
     * Get current page title
     */
    public String getPageTitle() {
        return driver.getTitle();
    }

    /**
     * Get current URL
     */
    public String getCurrentUrl() {
        return driver.getCurrentUrl();
    }

    /**
     * Get page source
     */
    public String getPageSource() {
        return driver.getPageSource();
    }
}

