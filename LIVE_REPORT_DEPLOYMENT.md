# 🔴 LIVE Report Deployment Guide

## 🎯 Goal
Make the report URL show **real-time updates** to everyone with the link.

**Live URL:** `https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html`

---

## 📋 Architecture

```
┌─────────────────┐
│  Your Computer  │ 
│  ProdSanity     │──┐
│  _Report.py     │  │ Saves data
└─────────────────┘  ↓
                 ┌──────────────┐
                 │  PostgreSQL  │ (Cloud hosted)
                 │   Database   │
                 └──────────────┘
                        ↑
                        │ Queries
                 ┌──────────────┐
                 │  Flask API   │ (Cloud hosted)
                 │  api_server  │
                 │    .py       │
                 └──────────────┘
                        ↑
                        │ HTTPS API calls
                 ┌──────────────┐
                 │  GitHub      │
                 │    Pages     │
                 │ live_report  │
                 │   .html      │
                 └──────────────┘
                        ↑
                        │ Users access
                 ┌──────────────┐
                 │   Everyone   │
                 │  with link   │
                 └──────────────┘
```

---

## ✅ Step 1: Deploy PostgreSQL Database (Cloud)

### **Option A: Azure Database for PostgreSQL** ⭐ Recommended

```powershell
# Install Azure CLI
winget install Microsoft.AzureCLI

# Login
az login

# Create resource group
az group create --name myisp-resources --location eastus

# Create PostgreSQL server
az postgres flexible-server create \
    --resource-group myisp-resources \
    --name myisp-postgres \
    --admin-user myadmin \
    --admin-password "YourPassword123!" \
    --sku-name Standard_B1ms \
    --tier Burstable \
    --version 15 \
    --storage-size 32 \
    --public-access 0.0.0.0

# Create database
az postgres flexible-server db create \
    --resource-group myisp-resources \
    --server-name myisp-postgres \
    --database-name myisp_tools

# Get connection string (save this!)
az postgres flexible-server show-connection-string \
    --server-name myisp-postgres \
    --database-name myisp_tools \
    --admin-user myadmin
```

**Connection String:**
```
postgresql://myadmin:YourPassword123!@myisp-postgres.postgres.database.azure.com/myisp_tools?sslmode=require
```

### **Option B: ElephantSQL (Free Tier)** ⚡ Quick Start

1. Go to: https://www.elephantsql.com/
2. Sign up (free)
3. Create new instance (Tiny Turtle - Free)
4. Get connection URL (copy it)

---

## ✅ Step 2: Deploy Flask API Server

### **Option A: Azure App Service** ⭐ Recommended

```powershell
# Create App Service plan
az appservice plan create \
    --name myisp-plan \
    --resource-group myisp-resources \
    --sku B1 \
    --is-linux

# Create web app
az webapp create \
    --resource-group myisp-resources \
    --plan myisp-plan \
    --name myisp-api \
   --runtime "PYTHON:3.11"

# Configure environment variables
az webapp config appsettings set \
    --resource-group myisp-resources \
    --name myisp-api \
    --settings \
        DB_HOST="myisp-postgres.postgres.database.azure.com" \
        DB_PORT="5432" \
        DB_NAME="myisp_tools" \
        DB_USER="myadmin" \
        DB_PASSWORD="YourPassword123!"

# Deploy code
cd C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report
az webapp up --name myisp-api --resource-group myisp-resources
```

**Your API URL:**
```
https://myisp-api.azurewebsites.net
```

### **Option B: Heroku** (Alternative)

```powershell
# Install Heroku CLI
winget install Heroku.HerokuCLI

# Login
heroku login

# Create app
heroku create myisp-api

# Add PostgreSQL
heroku addons:create heroku-postgresql:essential-0

# Deploy
git init
heroku git:remote -a myisp-api
git add api_server.py database_utils.py database_setup.sql requirements.txt
git commit -m "Deploy API"
git push heroku main
```

**Your API URL:**
```
https://myisp-api.herokuapp.com
```

### **Option C: Railway.app** ⚡ Fastest

1. Go to: https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Select `api_server.py` as entry point
6. Add PostgreSQL database from Railway
7. Copy the public URL

---

## ✅ Step 3: Update Live Report with API URL

Edit `live_report.html` line 194:

**Replace:**
```javascript
const API_BASE_URL = 'YOUR_API_URL_HERE';
```

**With your actual API URL:**
```javascript
const API_BASE_URL = 'https://myisp-api.azurewebsites.net';
```

---

## ✅ Step 4: Update Database Connection in api_server.py

Edit `database_utils.py` to use environment variables:

```python
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', '5432')),
    'database': os.getenv('DB_NAME', 'myisp_tools'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'postgres123')
}
```

---

## ✅ Step 5: Setup Database Schema on Cloud

```powershell
# Connect to cloud PostgreSQL
psql "postgresql://myadmin:YourPassword123!@myisp-postgres.postgres.database.azure.com/myisp_tools?sslmode=require"

# Run schema
\i C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report\database_setup.sql
```

---

## ✅ Step 6: Update Report Generator

Update `ProdSanity_Report.py` to save to cloud database instead of local:

**Option 1: Update .env file:**
```env
DB_HOST=myisp-postgres.postgres.database.azure.com
DB_PORT=5432
DB_NAME=myisp_tools
DB_USER=myadmin
DB_PASSWORD=YourPassword123!
```

**Option 2: Update database_utils.py directly** (if not using .env)

---

## ✅ Step 7: Deploy Live Report to GitHub Pages

```powershell
cd "C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report"

# Add live report to deployment
git add live_report.html
git commit -m "Add live auto-refreshing report"
git push
```

Update workflow to include `live_report.html`:
- File: `.github/workflows/deploy-github-pages.yml`
- Add: `cp live_report.html _site/`

---

## ✅ Step 8: Test Everything

### **1. Test API:**
```powershell
# Health check
Invoke-RestMethod https://myisp-api.azurewebsites.net/api/health

# Get latest data
Invoke-RestMethod https://myisp-api.azurewebsites.net/api/statistics/latest
```

### **2. Generate Report & Save to Cloud:**
```powershell
python ProdSanity_Report.py
```

### **3. Access Live Report:**
```
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

---

## 🎯 How It Works

1. **You run:** `python ProdSanity_Report.py` (locally)
2. **Script saves data to:** Cloud PostgreSQL database
3. **Flask API serves data from:** Cloud PostgreSQL
4. **GitHub Pages loads:** `live_report.html`
5. **JavaScript fetches data from:** Flask API (HTTPS)
6. **Report auto-refreshes:** Every 30 seconds (configurable)
7. **Everyone sees:** Same real-time data

---

## 🔄 Workflow After Setup

```powershell
# Every time you want to update the report:

# 1. Run report generator (saves to cloud DB)
python ProdSanity_Report.py

# 2. Share the link (data updates automatically)
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

**Users see updates immediately** - no need to push to GitHub!

---

## 📊 Features

✅ **Auto-refresh** every 30 seconds (configurable: 10s, 30s, 1min, 5min)  
✅ **Live indicator** (red pulse) shows real-time status  
✅ **Last updated** timestamp  
✅ **Manual refresh** button  
✅ **Export data** to JSON  
✅ **Connection status** indicator  
✅ **Error handling** with retry

---

## 💰 Cost Estimate

### **Azure (Recommended):**
- **PostgreSQL:** ~$7/month (Burstable B1ms)
- **App Service:** ~$13/month (B1 Basic)
- **Total:** ~$20/month

### **Free Options:**
- **ElephantSQL:** Free 20 MB PostgreSQL
- **Railway:** Free tier (500 hours/month)
- **Total:** $0/month

---

## 🐛 Troubleshooting

### Error: "Unable to Load Live Data"

**Check:**
1. API server is running: `curl https://myisp-api.azurewebsites.net/api/health`
2. Database has data: Run `python ProdSanity_Report.py`
3. CORS enabled in `api_server.py` (already done)
4. API URL in `live_report.html` is correct

### Error: "Connection refused"

**Fix:**
- Ensure cloud database allows connections from your IP
- Check firewall rules in Azure Portal

---

## 📖 Quick Reference

**Live Report URL:**
```
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

**API Endpoints:**
- Health: `/api/health`
- Stats: `/api/statistics/latest`
- Data: `/api/test-data/latest`
- All Reports: `/api/reports`

---

**🎉 Once deployed, everyone with the link sees live updates automatically!**

No need to regenerate HTML files or push to GitHub for data updates.
