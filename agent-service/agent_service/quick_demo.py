import os
import json
import argparse

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

FEATURE_DIR = os.path.join(REPO_ROOT, '..', 'src', 'test', 'resources', 'features')
PAGES_DIR = os.path.join(REPO_ROOT, '..', 'src', 'main', 'java', 'org', 'example', 'pages')

FEATURE_TEMPLATE = '''Feature: Generated from requirement

  Scenario: Auto generated login
    When I enter "standard_user" in "username" in "LoginPage"
    And I enter "secret_sauce" in "password" in "LoginPage"
    And I click "loginButton" on "LoginPage"
    Then "inventoryContainer" should be displayed on "InventoryPage"
'''

PAGE_LOGIN_TEMPLATE = '''package org.example.pages.{module};

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LoginPage extends BasePage {{

    // Generic locators (placeholder values)
    public By username = By.id("user-name");
    public By password = By.id("password");
    public By loginButton = By.id("login-button");

    public LoginPage(WebDriver driver) {{
        super(driver);
    }}
}}
'''

PAGE_INVENTORY_TEMPLATE = '''package org.example.pages.{module};

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class InventoryPage extends BasePage {{

    public By inventoryContainer = By.id("inventory_container");

    public InventoryPage(WebDriver driver) {{
        super(driver);
    }}
}}
'''


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_feature(module, filename='Generated.feature', content=None):
    path = os.path.join(FEATURE_DIR, module)
    ensure_dir(path)
    file_path = os.path.join(path, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content or FEATURE_TEMPLATE)
    return file_path


def write_pages(module):
    path = os.path.join(PAGES_DIR, module)
    ensure_dir(path)
    files = []
    login_path = os.path.join(path, 'LoginPage.java')
    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(PAGE_LOGIN_TEMPLATE.format(module=module))
    files.append(login_path)

    inv_path = os.path.join(path, 'InventoryPage.java')
    with open(inv_path, 'w', encoding='utf-8') as f:
        f.write(PAGE_INVENTORY_TEMPLATE.format(module=module))
    files.append(inv_path)
    return files


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', default='demo', help='Module name for generated files')
    parser.add_argument('--requirement', default='As a user I want to log in with username and password so I can access inventory', help='Requirement text')
    args = parser.parse_args()

    feat = write_feature(args.module)
    pages = write_pages(args.module)

    out = {
        'requirement': args.requirement,
        'written_features': [os.path.abspath(feat)],
        'written_pages': [os.path.abspath(p) for p in pages]
    }
    print(json.dumps(out, indent=2))

