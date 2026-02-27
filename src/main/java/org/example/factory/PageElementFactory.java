package org.example.factory;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

/**
 * PageElementFactory: Uses reflection to dynamically identify and interact with page elements
 * This factory allows for flexible page object creation without hardcoding element locators
 */
public class PageElementFactory {

    /**
     * Find element using reflection-based locator discovery
     * Method signature: getXXXElement() or isXXXPresent()
     */
    public static WebElement findElement(WebDriver driver, String elementName) {
        try {
            // Try different locator patterns
            By locator = getLocatorByName(elementName);
            if (locator != null) {
                return driver.findElement(locator);
            }
        } catch (Exception e) {
            throw new RuntimeException("Element not found: " + elementName, e);
        }
        return null;
    }

    /**
     * Dynamically resolve locators based on element name
     * Uses reflection to call locator methods
     */
    private static By getLocatorByName(String elementName) {
        // Convention-based locator resolution
        String id = camelToSnakeCase(elementName);

        // Try ID first
        try {
            return By.id(id);
        } catch (Exception e) {
            // Try XPath with element name
            return By.xpath("//*[@data-test='" + id + "']");
        }
    }

    /**
     * Convert camelCase to snake_case
     */
    private static String camelToSnakeCase(String str) {
        return str.replaceAll("([a-z])([A-Z])", "$1_$2").toLowerCase();
    }

    /**
     * Invoke method on page object using reflection
     */
    public static Object invokeMethod(Object pageObject, String methodName, Object... args)
            throws InvocationTargetException, IllegalAccessException {
        try {
            Class<?>[] parameterTypes = new Class<?>[args.length];
            for (int i = 0; i < args.length; i++) {
                parameterTypes[i] = args[i].getClass();
            }

            Method method = pageObject.getClass().getDeclaredMethod(methodName, parameterTypes);
            method.setAccessible(true);
            return method.invoke(pageObject, args);
        } catch (NoSuchMethodException e) {
            throw new RuntimeException("Method not found: " + methodName, e);
        }
    }

    /**
     * Get field value from page object using reflection
     */
    public static Object getFieldValue(Object pageObject, String fieldName)
            throws IllegalAccessException {
        try {
            var field = pageObject.getClass().getDeclaredField(fieldName);
            field.setAccessible(true);
            return field.get(pageObject);
        } catch (NoSuchFieldException e) {
            throw new RuntimeException("Field not found: " + fieldName, e);
        }
    }
}

