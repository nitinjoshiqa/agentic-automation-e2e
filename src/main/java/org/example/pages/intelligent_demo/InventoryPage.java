package org.example.pages.intelligent_demo;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * InventoryPage - Captured from: https://www.saucedemo.com/inventory.html
 * Real element locators discovered through intelligent page analysis
 */
public class InventoryPage extends BasePage {
    // Main inventory container
    public static final By INVENTORY_CONTAINER = By.id("inventory_container");

    // Product items list
    public static final By PRODUCT_ITEMS = By.className("inventory_item");

    // Add to cart buttons (class-based)
    public static final By ADD_TO_CART_BTN = By.cssSelector("button[data-test='add-to-cart-sauce-labs-backpack']");

    // Page title
    public static final By PAGE_TITLE = By.className("title");

    // Inventory label
    public static final By INVENTORY_LABEL = By.xpath("//span[contains(text(), 'Products')]");

    // First product name
    public static final By FIRST_PRODUCT_NAME = By.cssSelector(".inventory_item:first-child .inventory_item_name");

    // First product add button
    public static final By FIRST_PRODUCT_ADD = By.cssSelector(".inventory_item:first-child [data-test^='add-to-cart']");

    // Cart badge (item counter)
    public static final By CART_BADGE = By.className("shopping_cart_badge");

    // Cart icon
    public static final By CART_ICON = By.id("shopping_cart_container");

    public InventoryPage(WebDriver driver) {
        super(driver);
    }
}