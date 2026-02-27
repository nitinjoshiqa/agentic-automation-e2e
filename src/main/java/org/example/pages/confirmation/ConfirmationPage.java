package org.example.pages.confirmation;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * ConfirmationPage: Page object for order confirmation
 * Contains locators for generic step definitions only
 * All interactions handled by GenericStepDefinitions
 */
public class ConfirmationPage extends BasePage {

    // Locators - Public for generic step definitions
    public static final By SUCCESS_MESSAGE = By.className("complete-header");
    public static final By CONFIRMATION_ICON = By.className("pony_express");
    public static final By ORDER_SUMMARY_SECTION = By.className("complete-text");
    public static final By BACK_TO_PRODUCTS_BUTTON = By.id("back-to-products");
    public static final By LOGOUT_BUTTON = By.id("logout_sidebar_link");
    public static final By COMPANY_INFO = By.className("footer");
    public static final By SOCIAL_LINKS = By.className("social");
    public static final By DOWNLOAD_RECEIPT_BUTTON = By.id("download-receipt");
    public static final By ORDER_NUMBER = By.className("order-number");
    public static final By ITEMS_LIST = By.className("cart_item");
    public static final By FINAL_TOTAL = By.className("summary_total_label");

    public ConfirmationPage(WebDriver driver) {
        super(driver);
    }
}

