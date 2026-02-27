package org.example.pages.checkout;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * CheckoutSummaryPage: Page object for checkout summary
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class CheckoutSummaryPage extends BasePage {

    // Locators - Public for generic step definitions
    public static final By CHECKOUT_SUMMARY_TITLE = By.className("title");
    public static final By CART_ITEM = By.className("cart_item");
    public static final By ITEM_NAME = By.className("inventory_item_name");
    public static final By ITEM_PRICE = By.className("inventory_item_price");
    public static final By SUBTOTAL = By.className("summary_subtotal_label");
    public static final By TAX = By.className("summary_tax_label");
    public static final By TOTAL = By.className("summary_total_label");
    public static final By FINISH_BUTTON = By.id("finish");
    public static final By CANCEL_BUTTON = By.id("cancel");

    public CheckoutSummaryPage(WebDriver driver) {
        super(driver);
    }
}

