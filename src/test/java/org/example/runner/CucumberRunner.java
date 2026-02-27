package org.example.runner;

import io.cucumber.junit.Cucumber;
import io.cucumber.junit.CucumberOptions;
import org.junit.runner.RunWith;

/**
 * CucumberRunner: Test runner for executing Cucumber tests
 * Configures feature file location and reporting
 *
 * Generates:
 * - JSON for Allure reporting (cucumber-json-plugin)
 * - HTML for Cucumber reporting
 * - JUnit format for Maven Surefire
 */
@RunWith(Cucumber.class)
@CucumberOptions(
    features = "src/test/resources/features",
    glue = {"org.example.stepdefinitions", "org.example.hooks"},
    plugin = {
        "pretty",
        "html:target/cucumber-reports/cucumber.html",
        "json:target/allure-results/cucumber.json",
        "junit:target/surefire-reports/cucumber.xml",
        "io.qameta.allure.cucumber7jvm.AllureCucumber7Jvm"
    },
    monochrome = true,
    dryRun = false,
    stepNotifications = true
)
/**
 * Supports both specific and generic step definitions:
 * - Specific: LoginStepDefinitions, InventoryStepDefinitions, CartStepDefinitions
 * - Generic: GenericStepDefinitions (works with any page object using reflection)
 */
public class CucumberRunner {
}

