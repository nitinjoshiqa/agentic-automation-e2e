package org.example.pages.inventory;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * InventoryPage: Page object for inventory/products module
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class InventoryPage extends BasePage {

    // Locators - Public for generic step definitions
    public static final By INVENTORY_CONTAINER = By.className("inventory_list");
    public static final By PRODUCT_ITEMS = By.className("inventory_item");
    public static final By PRODUCT_NAME = By.className("inventory_item_name");
    public static final By PRODUCT_PRICE = By.className("inventory_item_price");
    public static final By PRODUCT_DESCRIPTION = By.className("inventory_item_desc");
    public static final By ADD_TO_CART_BUTTON = By.xpath("//button[contains(text(), 'Add to cart')]");
    public static final By REMOVE_FROM_CART_BUTTON = By.xpath("//button[contains(text(), 'Remove')]");
    public static final By SORT_DROPDOWN = By.cssSelector("[data-test='product_sort_container']");
    public static final By CART_BADGE = By.className("shopping_cart_badge");
    public static final By CART_LINK = By.className("shopping_cart_link");
    public static final By MENU_BUTTON = By.id("react-burger-menu-btn");
    public static final By LOGOUT_BUTTON = By.id("logout_sidebar_link");
    public static final By PRODUCT_IMAGE = By.xpath("//img[@class='inventory_item_img']");
    public static final By PRODUCT_RATING = By.className("product_rating");
    public static final By SORT_ATO_Z = By.xpath("//option[@value='az']");
    public static final By SORT_ZTO_A = By.xpath("//option[@value='za']");
    public static final By SORT_PRICE_LOW_HIGH = By.xpath("//option[@value='lohi']");
    public static final By SORT_PRICE_HIGH_LOW = By.xpath("//option[@value='hilo']");
    public static final By PRICE_FILTER_BUTTON = By.id("price_filter");
    public static final By MIN_PRICE = By.id("min_price");
    public static final By MAX_PRICE = By.id("max_price");
    public static final By APPLY_FILTER_BUTTON = By.id("apply_filter");

    public InventoryPage(WebDriver driver) {
        super(driver);
    }
}

