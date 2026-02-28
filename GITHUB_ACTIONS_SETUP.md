# GitHub Actions - Complete Setup Guide

## Overview

Your framework now has **two ways to run everything**:

### 1. **Local - Master Agent (Single Click)**
```bash
.\master-agent.ps1
```

### 2. **GitHub Actions - Fully Automated**
Push to GitHub → Tests run automatically → Report generated → Available on GitHub Pages

---

## Setup Instructions

### Step 1: Initialize Git Repository

```bash
cd D:\DreamProject\reflectioncucumber

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "chore: Initial commit with master agent and GitHub Actions"
```

### Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Create repository: `reflectioncucumber`
3. **DO NOT** initialize with README/license
4. Click Create

### Step 3: Connect Local to GitHub

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/reflectioncucumber.git

# Rename branch to main if needed
git branch -M main

# Push to GitHub
git push -u origin main
```

### Step 4: Enable GitHub Pages (Optional but Recommended)

1. Go to: https://github.com/YOUR_USERNAME/reflectioncucumber/settings/pages
2. Source: Deploy from branch
3. Branch: `gh-pages`
4. Click Save
5. Reports will be available at: `https://YOUR_USERNAME.github.io/reflectioncucumber`

---

## Using Master Agent Locally

### Full Flow (Everything)
```bash
.\master-agent.ps1
```
Output:
- Clean build
- Run 125 tests
- Generate Allure report
- Open in browser

### Test Only
```bash
.\master-agent.ps1 -Operation test
```

### Generate Report
```bash
.\master-agent.ps1 -Operation report
```

### Serve Report
```bash
.\master-agent.ps1 -Operation serve
```

### Generate from Requirement (RAG)
```bash
.\master-agent.ps1 -Operation generate -Requirement "User login and add to cart" -Project saucedemo
```

### Help
```bash
.\master-agent.ps1 -Operation help
```

---

## GitHub Actions Automated Flow

### What Happens When You Push

```
1. Push code to GitHub
   ↓
2. GitHub Actions triggers automatically
   ↓
3. Runs complete E2E flow:
   - Checkout code
   - Setup Java 11
   - Setup Python
   - Download dependencies
   - Run 125 tests
   - Generate Allure report
   - Upload artifacts
   - Deploy to GitHub Pages (optional)
   ↓
4. View results:
   - GitHub Actions tab (logs)
   - Artifacts (download report)
   - GitHub Pages (live report)
```

### Triggering Workflows

#### Automatic (No action needed)
```
• Push to main or develop
• Create pull request
• Daily at 2 AM (scheduled)
```

#### Manual (From GitHub UI)
1. Go to: Actions tab
2. Select: "E2E Test Automation with Allure Reports"
3. Click: "Run workflow"
4. Click: "Run workflow" again
5. Watch tests execute live!

---

## Viewing Results

### Option 1: GitHub Actions Tab
1. Go to: Actions tab
2. Click latest workflow run
3. See live logs
4. Download artifacts

### Option 2: Artifacts
1. Go to: Latest workflow run
2. Scroll down to Artifacts
3. Download: `allure-report` or `allure-results`
4. Extract and open `index.html`

### Option 3: GitHub Pages (if enabled)
1. Go to: https://YOUR_USERNAME.github.io/reflectioncucumber
2. View live report
3. Same as local report, but online!

---

## File Structure After Setup

```
reflectioncucumber/
├── .github/
│   └── workflows/
│       └── test-automation.yml      ← GitHub Actions config
├── src/
├── agent-service/
├── master-agent.ps1                ← Local orchestrator
├── pom.xml
├── README.md
├── HOW_TO_RUN.md
└── ... (other files)
```

---

## Workflow Features

### What It Does

✅ **Trigger on Events**
- Push to main/develop
- Pull requests
- Daily schedule (2 AM)
- Manual trigger

✅ **Build & Test**
- Java 11 setup
- Maven cache
- Dependency resolution
- 125 tests execution

✅ **Reporting**
- Allure report generation
- Test results JSON
- Artifacts upload
- GitHub Pages deployment

✅ **Notifications**
- GitHub Actions logs
- Build status
- Test summary

### Configuration

Edit: `.github/workflows/test-automation.yml`

**Change test schedule:**
```yaml
schedule:
  - cron: '0 2 * * *'  # Change this
```

**Change branches:**
```yaml
on:
  push:
    branches: [ main, develop ]  # Add/remove branches
```

---

## Environment Variables (If Needed)

Add secrets in: Settings → Secrets and variables

Example:
```yaml
- name: Run tests
  env:
    BROWSER: chrome
    TIMEOUT: 30
  run: mvn clean verify
```

---

## Troubleshooting

### Workflow Not Triggering
1. Check: `.github/workflows/test-automation.yml` exists
2. Ensure: Valid YAML syntax
3. Try: Manual trigger from Actions tab

### Tests Failing in GitHub but Pass Locally
1. Check: Java version match (11+)
2. Check: Maven cache
3. Add: `mvn clean` before tests

### Report Not Deploying to Pages
1. Enable: GitHub Pages in settings
2. Ensure: `gh-pages` branch exists
3. Check: Write permissions

---

## Quick Reference

| Operation | Command |
|-----------|---------|
| **Run Everything** | `.\master-agent.ps1` |
| **Test Only** | `.\master-agent.ps1 -Operation test` |
| **Generate Report** | `.\master-agent.ps1 -Operation report` |
| **View Help** | `.\master-agent.ps1 -Operation help` |
| **Push to GitHub** | `git push origin main` |
| **View Actions** | GitHub → Actions tab |
| **Download Report** | Actions → Artifacts |
| **Live Report** | https://YOUR_USERNAME.github.io/reflectioncucumber |

---

## Workflow Diagram

```
LOCAL DEVELOPMENT              GITHUB ACTIONS
─────────────────────────────────────────────────
                               
┌─────────────────┐           ┌──────────────────┐
│ master-agent.ps1│───────┬──→│ Push to GitHub   │
└─────────────────┘       │   └──────────────────┘
                          │            ↓
                          │   ┌──────────────────┐
                          │   │ Trigger Workflow │
                          │   └──────────────────┘
                          │            ↓
  Manual workflow ────────┴──→│ Test Execution │
  on Actions tab            │ 125 tests      │
                            └──────────────────┘
                                    ↓
                            ┌──────────────────┐
                            │ Generate Report  │
                            └──────────────────┘
                                    ↓
                     ┌──────────────┴──────────────┐
                     ↓                             ↓
            ┌─────────────────┐          ┌──────────────────┐
            │ Upload Artifacts│          │Deploy to Pages   │
            │ (for download)  │          │ (Live viewing)   │
            └─────────────────┘          └──────────────────┘
```

---

## Best Practices

✅ **Do:**
- Run locally before pushing
- Use meaningful commit messages
- Monitor GitHub Actions logs
- Review reports regularly
- Set schedule for daily runs

❌ **Don't:**
- Commit test failures without investigating
- Leave long-running workflows
- Hard-code sensitive data (use secrets instead)
- Ignore GitHub Actions notifications

---

## Next Steps

1. **Setup GitHub Repository**
   ```bash
   git init
   git remote add origin https://github.com/YOUR_USERNAME/reflectioncucumber.git
   git push -u origin main
   ```

2. **Enable GitHub Pages** (optional)
   - Settings → Pages → gh-pages branch

3. **Run Locally to Verify**
   ```bash
   .\master-agent.ps1
   ```

4. **Make a Test Push**
   ```bash
   git commit --allow-empty -m "test: trigger GitHub Actions"
   git push
   ```

5. **Monitor GitHub Actions**
   - Go to: Actions tab
   - Watch: Workflow execute
   - Download: Report

---

**Status: READY FOR GITHUB ACTIONS ✅**

Both local and automated testing are now configured!

