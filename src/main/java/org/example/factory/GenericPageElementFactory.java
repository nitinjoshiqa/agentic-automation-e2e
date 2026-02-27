package org.example.factory;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

/**
 * GenericPageElementFactory: Uses reflection to dynamically interact with page elements
 * Enables generic step definitions by discovering page objects, methods, and locators at runtime
 */
public class GenericPageElementFactory {

    /**
     * Cache for By locators to avoid repeated reflection
     */
    private static final Map<String, By> locatorCache = new HashMap<>();

    /**
     * Get locator from page object using reflection
     * Convention: public static final By locators named in UPPER_CASE
     * Searches up the class hierarchy if needed
     */
    public static By getLocator(Object pageObject, String locatorName) {
        String cacheKey = pageObject.getClass().getSimpleName() + "." + locatorName;

        if (locatorCache.containsKey(cacheKey)) {
            return locatorCache.get(cacheKey);
        }

        try {
            // Convert camelCase to UPPER_SNAKE_CASE for locator field names
            String fieldName = camelToSnakeCase(locatorName).toUpperCase();

            Field field = null;
            Class<?> currentClass = pageObject.getClass();

            // Search up the class hierarchy for the locator field
            while (currentClass != null && field == null) {
                try {
                    field = currentClass.getDeclaredField(fieldName);
                } catch (NoSuchFieldException e) {
                    currentClass = currentClass.getSuperclass();
                }
            }

            if (field == null) {
                throw new NoSuchFieldException("Locator field not found: " + fieldName);
            }

            field.setAccessible(true);
            By locator = (By) field.get(null);

            locatorCache.put(cacheKey, locator);
            return locator;
        } catch (NoSuchFieldException e) {
            throw new RuntimeException("Locator not found: " + locatorName +
                                     " in " + pageObject.getClass().getSimpleName(), e);
        } catch (IllegalAccessException e) {
            throw new RuntimeException("Cannot access locator: " + locatorName, e);
        }
    }

    /**
     * Enter text in an element using locator name
     */
    public static void enterText(Object pageObject, String locatorName, String text) {
        try {
            By locator = getLocator(pageObject, locatorName);
            WebDriver driver = getDriver(pageObject);
            WebElement element = driver.findElement(locator);
            element.clear();
            element.sendKeys(text);
        } catch (Exception e) {
            throw new RuntimeException("Failed to enter text in: " + locatorName, e);
        }
    }

    /**
     * Click on an element using locator name
     */
    public static void clickElement(Object pageObject, String locatorName) {
        try {
            By locator = getLocator(pageObject, locatorName);
            WebDriver driver = getDriver(pageObject);
            driver.findElement(locator).click();
        } catch (Exception e) {
            throw new RuntimeException("Failed to click element: " + locatorName, e);
        }
    }

    /**
     * Get text from an element using locator name
     */
    public static String getText(Object pageObject, String locatorName) {
        try {
            By locator = getLocator(pageObject, locatorName);
            WebDriver driver = getDriver(pageObject);
            return driver.findElement(locator).getText();
        } catch (Exception e) {
            throw new RuntimeException("Failed to get text from: " + locatorName, e);
        }
    }

    /**
     * Check if element is displayed using locator name
     */
    public static boolean isElementDisplayed(Object pageObject, String locatorName) {
        try {
            By locator = getLocator(pageObject, locatorName);
            WebDriver driver = getDriver(pageObject);
            return driver.findElement(locator).isDisplayed();
        } catch (Exception e) {
            return false;
        }
    }

    /**
     * Get attribute value from element using locator name
     */
    public static String getAttribute(Object pageObject, String locatorName, String attributeName) {
        try {
            By locator = getLocator(pageObject, locatorName);
            WebDriver driver = getDriver(pageObject);
            return driver.findElement(locator).getAttribute(attributeName);
        } catch (Exception e) {
            throw new RuntimeException("Failed to get attribute from: " + locatorName, e);
        }
    }

    /**
     * Invoke a method on page object using reflection
     */
    public static Object invokeMethod(Object pageObject, String methodName) {
        try {
            Method method = pageObject.getClass().getDeclaredMethod(methodName);
            method.setAccessible(true);
            return method.invoke(pageObject);
        } catch (Exception e) {
            throw new RuntimeException("Failed to invoke method: " + methodName, e);
        }
    }

    /**
     * Get WebDriver from page object using reflection
     * Searches up the class hierarchy if needed (for inherited fields from BasePage)
     */
    private static WebDriver getDriver(Object pageObject) {
        try {
            Field driverField = null;
            Class<?> currentClass = pageObject.getClass();

            // Search up the class hierarchy for the driver field
            while (currentClass != null && driverField == null) {
                try {
                    driverField = currentClass.getDeclaredField("driver");
                } catch (NoSuchFieldException e) {
                    currentClass = currentClass.getSuperclass();
                }
            }

            if (driverField == null) {
                throw new NoSuchFieldException("driver field not found in class hierarchy");
            }

            driverField.setAccessible(true);
            return (WebDriver) driverField.get(pageObject);
        } catch (Exception e) {
            throw new RuntimeException("Failed to get WebDriver from page object", e);
        }
    }

    /**
     * Convert camelCase to snake_case
     */
    private static String camelToSnakeCase(String str) {
        return str.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase();
    }

    /**
     * Clear locator cache (useful for testing)
     */
    public static void clearCache() {
        locatorCache.clear();
    }
}

