package org.example.pages.demo;

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class InventoryPage extends BasePage {
    public static final By INVENTORY_CONTAINER = By.id("inventory_container");
    public static final By PRODUCTS = By.className("inventory_item");
    public static final By ADD_TO_CART = By.className("btn_primary");

    public InventoryPage(WebDriver driver) {
        super(driver);
    }
}