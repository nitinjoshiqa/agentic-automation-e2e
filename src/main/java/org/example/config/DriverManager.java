package org.example.config;

import io.github.bonigarcia.wdm.WebDriverManager;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * DriverManager: Singleton pattern for WebDriver management
 * Handles browser initialization and cleanup
 */
public class DriverManager {
    private static DriverManager instance;
    private WebDriver driver;

    private DriverManager() {
    }

    public static synchronized DriverManager getInstance() {
        if (instance == null) {
            instance = new DriverManager();
        }
        return instance;
    }

    /**
     * Initialize Chrome WebDriver
     */
    public WebDriver initializeDriver() {
        if (driver == null) {
            WebDriverManager.chromedriver().setup();
            ChromeOptions options = new ChromeOptions();
            options.addArguments("--disable-blink-features=AutomationControlled");
            options.addArguments("--disable-dev-shm-usage");
            options.addArguments("--no-sandbox");
            driver = new ChromeDriver(options);
            driver.manage().window().maximize();
        }
        return driver;
    }

    /**
     * Get the current WebDriver instance
     */
    public WebDriver getDriver() {
        if (driver == null) {
            return initializeDriver();
        }
        return driver;
    }

    /**
     * Quit the WebDriver
     */
    public void quitDriver() {
        if (driver != null) {
            driver.quit();
            driver = null;
        }
    }

    /**
     * Close the driver instance reference
     */
    public static void reset() {
        if (instance != null && instance.driver != null) {
            instance.driver.quit();
            instance.driver = null;
        }
        instance = null;
    }
}

