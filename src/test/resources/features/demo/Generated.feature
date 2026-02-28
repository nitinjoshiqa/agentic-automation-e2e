Feature: Generated from requirement

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

  Scenario: Failed login with invalid password
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "wrong_password" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "errorMessage" should be displayed on "LoginPage"
