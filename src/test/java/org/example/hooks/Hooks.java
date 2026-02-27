package org.example.hooks;

import io.cucumber.java.Before;
import io.cucumber.java.After;
import org.example.context.ScenarioContext;
import org.example.pages.login.LoginPage;

/**
 * Hooks: Global hooks for Cucumber scenarios
 * Handles setup and teardown for each scenario
 */
public class Hooks {
    private ScenarioContext scenarioContext;

    // Added no-argument constructor for Serenity/Cucumber object factory
    public Hooks() {
        // Fall back to a default ScenarioContext if DI is not provided
        this(new ScenarioContext());
    }

    public Hooks(ScenarioContext scenarioContext) {
        this.scenarioContext = scenarioContext;
    }

    @Before
    public void setUp() {
        System.out.println("========== Test Execution Started ==========");
        // Navigate to login page before each scenario
        LoginPage loginPage = scenarioContext.getLoginPage();
        loginPage.navigateToLoginPage();
    }

    @After
    public void tearDown() {
        System.out.println("========== Test Execution Ended ==========");
        scenarioContext.cleanup();
    }
}
