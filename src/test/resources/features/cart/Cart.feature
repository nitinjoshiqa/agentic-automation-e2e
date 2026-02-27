Feature: Shopping Cart Management
  As a shopper
  I want to manage items in my cart
  So that I can review and proceed to checkout

  Scenario: View cart with items
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "cartLink" on "InventoryPage"
    Then "cartTitle" should be displayed on "CartPage"
    And "cartItem" should be displayed on "CartPage"

  Scenario: Remove item from cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "cartLink" on "InventoryPage"
    And I click "removeButton" on "CartPage"
    Then "cartItem" should not be displayed on "CartPage"

  Scenario: Continue shopping from cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "cartLink" on "InventoryPage"
    And I click "continueShoppingButton" on "CartPage"
    Then "inventoryContainer" should be displayed on "InventoryPage"

  Scenario: Proceed to checkout from cart
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    And I click "addToCartButton" on "InventoryPage"
    And I click "cartLink" on "InventoryPage"
    And I click "checkoutButton" on "CartPage"
    Then "checkoutButton" should not be displayed on "CartPage"

