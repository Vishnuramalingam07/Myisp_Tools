# 🚂 Railway.app Deployment Guide (FREE)

## ⚡ Why Railway.app?
- ✅ **100% FREE** for hobby projects
- ✅ PostgreSQL database included
- ✅ Auto-deploys from GitHub
- ✅ No credit card required
- ✅ Simple setup (5 minutes)

---

## 🚀 Deployment Steps

### **Step 1: Create Railway Account**

1. Go to: https://railway.app/
2. Click **"Start a New Project"**
3. Sign in with GitHub
4. Authorize Railway to access your repositories

---

### **Step 2: Create PostgreSQL Database**

1. Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
2. Wait for database to provision (~30 seconds)
3. Click on the database
4. Go to **"Variables"** tab
5. **Copy these values:**
   - `PGHOST` (Database host)
   - `PGPORT` (Usually 5432)
   - `PGDATABASE` (Database name)
   - `PGUSER` (Username)
   - `PGPASSWORD` (Password)

---

### **Step 3: Run Database Schema**

**Option A: Via Railway CLI**
```powershell
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run schema
railway run psql -f database_setup.sql
```

**Option B: Via Connection String**
```powershell
# Get connection string from Railway dashboard
$connString = "postgresql://user:pass@host:port/database"

# Run schema
psql "$connString" -f database_setup.sql
```

---

### **Step 4: Deploy Flask API**

1. In Railway dashboard, click **"+ New"** → **"GitHub Repo"**
2. Select your **Myisp_Tools** repository
3. Railway will auto-detect Python and `api_server.py`
4. Click **"Deploy"**

---

### **Step 5: Configure Environment Variables**

1. Click on your web service (api_server)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add these (use values from Step 2):

```
DB_HOST = <PGHOST from database>
DB_PORT = <PGPORT from database>
DB_NAME = <PGDATABASE from database>
DB_USER = <PGUSER from database>
DB_PASSWORD = <PGPASSWORD from database>
```

5. Click **"Deploy"** to restart with new variables

---

### **Step 6: Get Your API URL**

1. Click on your web service
2. Go to **"Settings"** tab
3. Scroll to **"Domains"**
4. Click **"Generate Domain"**
5. **Copy the URL** (e.g., `https://myisp-api.railway.app`)

---

### **Step 7: Update live_report.html**

Edit `live_report.html` line 194:

**Replace:**
```javascript
const API_BASE_URL = 'YOUR_API_URL_HERE';
```

**With your Railway URL:**
```javascript
const API_BASE_URL = 'https://myisp-api.railway.app';
```

---

### **Step 8: Push to GitHub**

```powershell
cd "C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report"

git add live_report.html railway.json Procfile
git commit -m "Configure Railway deployment"
git push
```

---

### **Step 9: Update Local Script to Use Cloud DB**

Update your `.env` file:

```env
# Railway PostgreSQL (replace with actual values from Railway)
DB_HOST=containers-us-west-xxx.railway.app
DB_PORT=7432
DB_NAME=railway
DB_USER=postgres
DB_PASSWORD=your-password-from-railway
```

---

### **Step 10: Test Everything**

**1. Test API:**
```powershell
# Health check
Invoke-RestMethod https://myisp-api.railway.app/api/health

# Get statistics
Invoke-RestMethod https://myisp-api.railway.app/api/statistics/latest
```

**2. Generate Report:**
```powershell
python ProdSanity_Report.py
```
(This will save data to Railway's PostgreSQL)

**3. View Live Report:**
```
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

---

## ✅ Complete Architecture

```
┌─────────────────────────────────────┐
│  Your Computer                       │
│  - ProdSanity_Report.py             │
│  - Saves data to Railway DB         │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Railway.app (FREE)                  │
│  - PostgreSQL Database              │
│  - Flask API (api_server.py)        │
│  - URL: https://xxx.railway.app     │
└──────────────┬──────────────────────┘
               │
               ↑ API Calls (HTTPS)
               │
┌─────────────────────────────────────┐
│  GitHub Pages (FREE)                 │
│  - live_report.html                 │
│  - Auto-refreshes every 30s         │
│  - URL: github.io/Myisp_Tools/      │
└──────────────┬──────────────────────┘
               │
               ↓
┌─────────────────────────────────────┐
│  Users Access                        │
│  - See live updates                 │
│  - No installation needed           │
└─────────────────────────────────────┘
```

---

## 📊 Free Tier Limits

**Railway.app FREE Plan:**
- ✅ $5 free credits per month
- ✅ ~500 hours of uptime
- ✅ 1 GB RAM
- ✅ 1 GB Disk
- ✅ PostgreSQL database included
- ✅ No credit card required initially

**Enough for:**
- Hobby projects
- Testing/Demo
- Small team usage
- ~20 report generations per day

---

## 🐛 Troubleshooting

### Error: "Build failed"
**Fix:** Ensure `requirements.txt` includes all dependencies:
```
flask>=3.0.0
flask-cors>=4.0.0
psycopg2-binary>=2.9.9
python-dotenv>=1.0.0
```

### Error: "Cannot connect to database"
**Fix:** 
1. Check environment variables in Railway dashboard
2. Verify database is running (should show green status)
3. Check logs in Railway dashboard

### API returns empty data
**Fix:**
1. Run `python ProdSanity_Report.py` to populate database
2. Check logs: Railway dashboard → API service → "Logs" tab

---

## 🔄 Workflow After Setup

```powershell
# 1. Generate new report (saves to Railway)
python ProdSanity_Report.py

# 2. Share the link
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html

# 3. Everyone sees live updates automatically!
```

No need to push to GitHub for data updates - only for code changes.

---

## 💰 Cost Summary

| Component | Service | Cost |
|-----------|---------|------|
| Frontend (HTML/JS) | GitHub Pages | **FREE** |
| Backend (Flask API) | Railway.app | **FREE** |
| Database (PostgreSQL) | Railway.app | **FREE** |
| **Total** | | **$0/month** ✅ |

---

## 🎉 Benefits

✅ **Zero cost** for hosting  
✅ **Auto-deploys** when you push to GitHub  
✅ **Live updates** for all users  
✅ **No server management** required  
✅ **HTTPS** by default  
✅ **PostgreSQL** included  

---

**🚀 Ready to deploy? Follow the steps above!**
