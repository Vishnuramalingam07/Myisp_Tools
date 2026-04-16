# 🌐 GitHub Pages Deployment Guide

## 📋 Overview

This guide explains how to deploy your Azure DevOps Test Execution Report Generator to GitHub Pages.

**What Gets Deployed:**
- ✅ Static HTML demo dashboard  
- ✅ Sample generated reports
- ✅ Documentation (README, Quick Start Guide)
- ❌ Flask API server (requires separate hosting)
- ❌ PostgreSQL database (requires separate hosting)
- ❌ Python report generator (runs locally)

---

## 🚀 Deployment Options

### **Option 1: Automated Deployment (GitHub Actions)** ⭐ Recommended

This automatically deploys your static files whenever you push to the `main` branch.

#### Steps:

1. **Enable GitHub Pages in Repository Settings**
   ```
   1. Go to your repository on GitHub
   2. Click "Settings" → "Pages"
   3. Under "Source", select "GitHub Actions"
   4. Save
   ```

2. **GitHub Actions workflow already created**
   - File: `.github/workflows/deploy-github-pages.yml`
   - Automatically deploys on push to `main` branch
   - No further action needed!

3. **Push your code**
   ```powershell
   git add .
   git commit -m "Add GitHub Pages deployment"
   git push origin main
   ```

4. **Access your site**
   - Wait 2-3 minutes for deployment
   - Your site will be at: `https://YOUR_USERNAME.github.io/MyISP_Tools/Prod_Sanity_Report/`

---

### **Option 2: Manual GitHub Pages Setup**

Deploy using GitHub's built-in Pages feature without automation.

#### Steps:

1. **Create a `gh-pages` branch**
   ```powershell
   git checkout -b gh-pages
   ```

2. **Copy only static files**
   ```powershell
   # Keep only these files in gh-pages branch:
   - index.html
   - demo_dashboard.html
   - sample_reports.html
   - Production_execution_report_*.html
   - README.md
   - QUICK_START.md
   - SETUP_GUIDE.md
   ```

3. **Remove backend files** (Optional - keep for reference)
   ```powershell
   # These won't work on GitHub Pages anyway:
   git rm api_server.py
   git rm database_*.py
   git rm database_setup.sql
   git rm ProdSanity_Report.py
   git rm setup.bat setup.sh
   ```

4. **Commit and push**
   ```powershell
   git add .
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

5. **Enable GitHub Pages**
   - Go to repository Settings → Pages
   - Source: `gh-pages` branch, `/root` folder
   - Save

6. **Access your site**
   - URL: `https://YOUR_USERNAME.github.io/MyISP_Tools/Prod_Sanity_Report/`

---

## 🎯 What's Deployed

### **Landing Page** (`index.html`)
Main entry point with navigation to:
- Demo dashboard
- Sample reports
- Documentation

### **Demo Dashboard** (`demo_dashboard.html`)
Interactive dashboard with:
- Sample test execution data
- Visual statistics
- Mock data (no backend required)

### **Sample Reports** (`sample_reports.html`)
Gallery of:
- Pre-generated HTML reports
- Documentation links
- Setup guides

### **Documentation**
- `README.md` - Complete project overview
- `QUICK_START.md` - Quick setup guide
- `SETUP_GUIDE.md` - Detailed setup instructions

---

## 🔧 Configuration

### Update GitHub URLs

Before deploying, update placeholder URLs in your HTML files:

**Files to update:**
- `index.html` (line 227)
- `sample_reports.html` (line 198)

**Replace:**
```html
https://github.com/YOUR_USERNAME/MyISP_Tools
```

**With:**
```html
https://github.com/YOUR_ACTUAL_USERNAME/MyISP_Tools
```

**Quick fix:**
```powershell
# PowerShell command to replace in all files:
(Get-Content index.html) -replace 'YOUR_USERNAME', 'your-actual-username' | Set-Content index.html
(Get-Content sample_reports.html) -replace 'YOUR_USERNAME', 'your-actual-username' | Set-Content sample_reports.html
```

---

## 📊 Full Stack Deployment (Backend + Frontend)

To deploy the **complete application** with live data:

### **Frontend: GitHub Pages** (Static files)
- Deploy HTML/CSS/JS as shown above
- Modify `dynamic_report.html` to call hosted API

### **Backend: Cloud Services** (Choose one)

#### **Option A: Azure App Service** ⭐ Recommended for Azure users
```powershell
# 1. Install Azure CLI
winget install Microsoft.AzureCLI

# 2. Login to Azure
az login

# 3. Create App Service
az webapp up --name myisp-api --resource-group my-resource-group --runtime PYTHON:3.9

# 4. Deploy Flask API
# (API will be available at: https://myisp-api.azurewebsites.net)
```

#### **Option B: Heroku**
```powershell
# 1. Install Heroku CLI
winget install Heroku.HerokuCLI

# 2. Create app
heroku create myisp-api

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 4. Deploy
git push heroku main
```

#### **Option C: Railway.app**
```powershell
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Initialize and deploy
railway init
railway up
```

### **Update Frontend to Use Hosted API**

Edit `dynamic_report.html`:
```javascript
// Change API URL from:
const API_BASE_URL = 'http://localhost:5000';

// To your hosted API:
const API_BASE_URL = 'https://myisp-api.azurewebsites.net';
```

---

## 🐛 Troubleshooting

### 404 Error - Page Not Found
**Solution:** Ensure your GitHub Pages source is set correctly in repository settings.

### Blank Page
**Solution:** Check browser console (F12) for JavaScript errors. Verify file paths are correct.

### CORS Error (when calling external API)
**Solution:** Add CORS headers to your API server (already done in `api_server.py`).

### Changes Not Showing
**Solution:**
```powershell
# Clear browser cache or use Ctrl+Shift+R (hard refresh)
# Wait 5-10 minutes for GitHub Pages cache to update
```

---

## 📚 Additional Resources

- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Azure App Service Python Apps](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Heroku Python Support](https://devcenter.heroku.com/articles/getting-started-with-python)

---

## ✅ Deployment Checklist

- [ ] GitHub repository created and code pushed
- [ ] Placeholder URLs updated with actual GitHub username
- [ ] GitHub Pages enabled in repository settings
- [ ] GitHub Actions workflow file present (`.github/workflows/deploy-github-pages.yml`)
- [ ] Code pushed to `main` branch
- [ ] Wait 2-3 minutes for deployment
- [ ] Visit site URL to verify
  - [ ] Landing page loads correctly
  - [ ] Demo dashboard works
  - [ ] Sample reports are accessible
  - [ ] Documentation links work
- [ ] (Optional) Backend API deployed to cloud service
- [ ] (Optional) Frontend updated to use hosted API URL

---

## 🎉 Success!

Once deployed, your site will be accessible at:

```
https://YOUR_USERNAME.github.io/MyISP_Tools/Prod_Sanity_Report/
```

**Share this URL with your team** to showcase your Azure DevOps test reporting solution!

---

## 📧 Support

If you encounter issues during deployment:

1. Check GitHub Actions logs: Repository → Actions tab
2. Review browser console (F12) for errors
3. Verify all file paths are correct (case-sensitive on GitHub Pages)
4. Ensure no backend dependencies in static pages

---

**Made with ❤️ for better test reporting**
