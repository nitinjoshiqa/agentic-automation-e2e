Feature: Product Inventory Management
  As a logged-in user
  I want to view and manage products
  So that I can select items to purchase

  Scenario: View inventory page with products
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "inventoryContainer" should be displayed on "InventoryPage"

  Scenario: Add single product to cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    Then "cartBadge" should be displayed on "InventoryPage"

  Scenario: Add multiple products to cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "addToCartButton" on "InventoryPage"
    Then "cartBadge" should be displayed on "InventoryPage"

  Scenario: Remove product from cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "removeFromCartButton" on "InventoryPage"
    Then "cartBadge" should not be displayed on "InventoryPage"

  Scenario: Navigate to cart from inventory
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "cartLink" on "InventoryPage"
    Then "cartTitle" should be displayed on "CartPage"

