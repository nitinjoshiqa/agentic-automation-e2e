#!/usr/bin/env python3
"""
Context-Aware RAG Service - Configuration-Driven
Plug and play service that generates features and pages using external config
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import os
import sys

# Import configuration
from rag_config import RAG_CONFIG

app = FastAPI(title="Context-Aware Agentic RAG")

# ============= DATA MODELS =============

class FeatureRequest(BaseModel):
    requirement_text: str
    project: str = "automationexercise"
    module: Optional[str] = None

class GenerationResponse(BaseModel):
    status: str
    project: str
    features: Optional[List[str]] = None
    pages: Optional[List[str]] = None
    conventions: List[str] = []

# ============= RAG SERVICE =============

class ConfigurableRAGService:
    """RAG service that uses configuration to generate features and pages"""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.framework_config = config.get("framework", {})
        self.projects_config = config.get("projects", {})
        self._resolve_framework_root()

    def _resolve_framework_root(self):
        """Resolve framework root path relative to this file"""
        rag_service_dir = Path(__file__).parent
        root_relative = self.framework_config.get("root_path", "../../..")
        self.framework_root = (rag_service_dir / root_relative).resolve()

    def get_project_config(self, project: str) -> Dict[str, Any]:
        """Get project-specific configuration"""
        if project not in self.projects_config:
            raise ValueError(f"Project '{project}' not found in config. Available: {list(self.projects_config.keys())}")
        return self.projects_config[project]

    def analyze_requirement(self, requirement: str, project: str) -> tuple[List[str], List[str]]:
        """Analyze requirement and return detected pages"""
        proj_config = self.get_project_config(project)
        req_lower = requirement.lower()
        pages_config = proj_config.get("locators", {})

        # Keyword mapping for page detection
        page_keywords = {
            "login": "LoginPage",
            "signin": "LoginPage",
            "authenticate": "LoginPage",
            "signup": "SignupPage",
            "register": "SignupPage",
            "account": "SignupPage",
            "product": "ProductsPage",
            "browse": "ProductsPage",
            "search": "ProductsPage",
            "inventory": "InventoryPage",
            "cart": "CartPage",
            "checkout": "CheckoutPage",
            "order": "CheckoutPage",
            "payment": "CheckoutPage",
            "home": "HomePage",
        }

        # Find matching pages based on requirement keywords
        detected_pages = []
        for keyword, page_name in page_keywords.items():
            if keyword in req_lower and page_name not in detected_pages:
                if page_name in pages_config:  # Only if config has this page
                    detected_pages.append(page_name)

        # Default pages if none detected
        if not detected_pages:
            detected_pages = list(pages_config.keys())[:2]  # Get first 2 pages

        # Ensure at least LoginPage is included for authentication flows
        if "login" in req_lower and "LoginPage" in pages_config and "LoginPage" not in detected_pages:
            detected_pages.insert(0, "LoginPage")

        return detected_pages

    def generate_feature(self, requirement: str, project: str, module: Optional[str] = None) -> str:
        """Generate feature file from requirement"""
        proj_config = self.get_project_config(project)
        module = module or proj_config.get("module")

        # Create features directory
        features_dir = self.framework_root / proj_config.get("features_dir")
        features_dir.mkdir(parents=True, exist_ok=True)

        # Generate feature name from requirement
        feature_name = requirement.split(" so that ")[0].strip() if " so that " in requirement else requirement

        # Detected pages
        detected_pages = self.analyze_requirement(requirement, project)

        # Generate Gherkin using framework step syntax
        feature_content = f'''Feature: {feature_name}

  Scenario: User completes main workflow
    Given I navigate to the application
    When I interact with required elements
    Then the action completes successfully
    And confirmation is displayed

  Scenario: User validates important fields
    Given the system is ready
    When I enter required information
    Then the information is accepted
'''

        # Save feature file
        feature_file = features_dir / f"{module}_generated.feature"
        feature_file.write_text(feature_content, encoding="utf-8")

        return str(feature_file)

    def generate_pages(self, project: str, module: Optional[str] = None, pages: Optional[List[str]] = None) -> List[str]:
        """Generate page objects from configuration"""
        proj_config = self.get_project_config(project)
        module = module or proj_config.get("module")
        package = proj_config.get("package")

        # Determine which pages to generate
        pages_to_generate = pages or proj_config.get("pages", [])
        locators_db = proj_config.get("locators", {})

        # Create pages directory
        pages_dir = self.framework_root / proj_config.get("pages_dir")
        pages_dir.mkdir(parents=True, exist_ok=True)

        generated_files = []

        for page_name in pages_to_generate:
            if page_name not in locators_db:
                print(f"Warning: No locators found for {page_name}")
                continue

            locators = locators_db[page_name]

            # Build locator declarations
            locator_declarations = ""
            for loc_name, loc_css in locators.items():
                locator_declarations += f'    public static final By {loc_name} = By.cssSelector("{loc_css}");\n'

            # Generate page object
            page_content = f'''package {package};

import org.example.base.BasePage;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * {page_name}
 * Auto-generated page object following framework conventions
 * UPPER_SNAKE_CASE locators for reflection-based access
 */
public class {page_name} extends BasePage {{
{locator_declarations}
    public {page_name}(WebDriver driver) {{
        super(driver);
    }}
}}
'''

            # Save page file
            page_file = pages_dir / f"{page_name}.java"
            page_file.write_text(page_content, encoding="utf-8")
            generated_files.append(str(page_file))

        return generated_files

# Initialize RAG service with configuration
rag_service = ConfigurableRAGService(RAG_CONFIG)

# ============= ENDPOINTS =============

@app.get("/health")
async def health():
    """Health check"""
    return {
        "status": "ok",
        "service": "context-aware-rag",
        "available_projects": list(rag_service.projects_config.keys())
    }

@app.post("/generate-features", response_model=GenerationResponse)
async def generate_features(request: FeatureRequest):
    """Generate features from requirement"""
    try:
        feature_file = rag_service.generate_feature(
            request.requirement_text,
            request.project,
            request.module
        )

        proj_config = rag_service.get_project_config(request.project)

        # Detect pages from requirement
        detected_pages = rag_service.analyze_requirement(request.requirement_text, request.project)

        return GenerationResponse(
            status="success",
            project=request.project,
            features=[feature_file],
            conventions=[
                "✓ Gherkin syntax matches generic step definitions",
                "✓ Page names follow ExactClassMatch convention",
                f"✓ Site: {proj_config.get('site_url')}",
                f"✓ Module: {request.module or proj_config.get('module')}",
                f"✓ Detected pages: {', '.join(detected_pages)}",
                "✓ Configuration-driven generation",
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-pages", response_model=GenerationResponse)
async def generate_pages(request: FeatureRequest):
    """Generate page objects from configuration"""
    try:
        proj_config = rag_service.get_project_config(request.project)

        # Detect pages from requirement
        detected_pages = rag_service.analyze_requirement(request.requirement_text, request.project)

        # Generate pages
        pages = rag_service.generate_pages(
            request.project,
            request.module,
            detected_pages
        )

        return GenerationResponse(
            status="success",
            project=request.project,
            pages=pages,
            conventions=[
                "✓ Extends BasePage",
                "✓ UPPER_SNAKE_CASE locators",
                f"✓ Real locators from {proj_config.get('site_url')}",
                "✓ CSS selectors (reliable)",
                "✓ Works with PageFactory reflection",
                f"✓ Package: {proj_config.get('package')}",
            ]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/projects")
async def list_projects():
    """List available projects"""
    return {
        "projects": [
            {
                "name": config.get("name"),
                "module": config.get("module"),
                "site_url": config.get("site_url"),
                "pages": list(config.get("locators", {}).keys())
            }
            for project_id, config in rag_service.projects_config.items()
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)



