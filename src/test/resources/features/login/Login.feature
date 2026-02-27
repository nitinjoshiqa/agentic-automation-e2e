Feature: User Login Functionality
  As a user
  I want to login to SauceDemo application
  So that I can access the product catalog

  Scenario: Successful login with valid credentials
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "loginButton" should not be displayed on "LoginPage"

  Scenario: Failed login with invalid username
    When I enter "invalid_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "errorMessage" should be displayed on "LoginPage"
    And "errorMessage" on "LoginPage" should contain "Username and password"

  Scenario: Failed login with invalid password
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "wrong_password" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "errorMessage" should be displayed on "LoginPage"
    And "loginButton" should be displayed on "LoginPage"

  Scenario: Step-by-step login process
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "loginButton" should not be displayed on "LoginPage"

  Scenario: Verify login page elements
    Then "username" should be displayed on "LoginPage"
    And "password" should be displayed on "LoginPage"
    And "loginButton" should be displayed on "LoginPage"

