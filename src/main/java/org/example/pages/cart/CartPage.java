package org.example.pages.cart;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * CartPage: Page object for cart module
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class CartPage extends BasePage {

    // Locators - Public for generic step definitions
    public static final By CART_ITEM = By.className("cart_item");
    public static final By ITEM_NAME = By.className("inventory_item_name");
    public static final By ITEM_PRICE = By.className("inventory_item_price");
    public static final By ITEM_QUANTITY = By.className("cart_quantity");
    public static final By ITEM_TOTAL_PRICE = By.className("inventory_item_price");
    public static final By REMOVE_BUTTON = By.xpath("//button[contains(text(), 'Remove')]");
    public static final By CHECKOUT_BUTTON = By.id("checkout");
    public static final By CONTINUE_SHOPPING_BUTTON = By.id("continue-shopping");
    public static final By CART_TITLE = By.className("title");
    public static final By EMPTY_CART_MESSAGE = By.className("empty_message");
    public static final By INCREASE_QUANTITY_BUTTON = By.xpath("//button[contains(@class, 'increment')]");
    public static final By DECREASE_QUANTITY_BUTTON = By.xpath("//button[contains(@class, 'decrement')]");
    public static final By SUBTOTAL = By.className("summary_subtotal_label");
    public static final By TAX = By.className("summary_tax_label");
    public static final By GRAND_TOTAL = By.className("summary_total_label");
    public static final By MENU_BUTTON = By.id("react-burger-menu-btn");
    public static final By LOGOUT_BUTTON = By.id("logout_sidebar_link");
    public static final By CART_BADGE = By.className("shopping_cart_badge");

    public CartPage(WebDriver driver) {
        super(driver);
    }
}

