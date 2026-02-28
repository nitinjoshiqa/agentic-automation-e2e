Feature: User Login and Inventory Access

  Background:
    Given I open the application
    And I am on the login page

  Scenario: Successful login with valid credentials
    When I enter "standard_user" in "username" field
    And I enter "secret_sauce" in "password" field
    And I click the "login" button
    Then I should see the inventory page
    And the page title should contain "Products"

  Scenario: Failed login with invalid username
    When I enter "invalid_user" in "username" field
    And I enter "secret_sauce" in "password" field
    And I click the "login" button
    Then I should see an error message
    And error should contain "Username"

  Scenario: Failed login with invalid password
    When I enter "standard_user" in "username" field
    And I enter "wrong_password" in "password" field
    And I click the "login" button
    Then I should see an error message
    And the login form should still be visible
