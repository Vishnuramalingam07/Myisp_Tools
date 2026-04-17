# ☁️ Google Cloud Run Deployment Guide

## 📋 Prerequisites

1. **Google Cloud Account** (Free tier: 2M requests/month)
   - Sign up: https://cloud.google.com/free

2. **Google Cloud SDK**
   - Download: https://cloud.google.com/sdk/docs/install
   - Install and restart PowerShell

3. **Docker Desktop** (Optional - Cloud Run can build for you!)
   - Download: https://www.docker.com/products/docker-desktop/

---

## 🚀 Quick Deploy (Easiest - No Docker Required!)

### **Step 1: Install Google Cloud SDK**

```powershell
# Download and run installer:
https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe

# After installation, restart PowerShell and initialize:
gcloud init
```

**Follow prompts:**
- Login with your Google account
- Create new project or select existing one
- Set default region (e.g., `us-central1`)

---

### **Step 2: Enable Required APIs**

```powershell
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API (for building images)
gcloud services enable cloudbuild.googleapis.com
```

---

### **Step 3: Set Environment Variables (Azure DevOps Credentials)**

```powershell
# Set your Azure DevOps credentials as Cloud Run secrets
# Replace with your actual values:

$env:ADO_ORG="your-ado-organization"
$env:ADO_PROJECT="your-ado-project"  
$env:ADO_PAT="your-personal-access-token"
```

---

### **Step 4: Deploy to Cloud Run**

```powershell
# Deploy from source (Cloud Run will build Docker image for you!)
gcloud run deploy prodreport-refresh `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars="ADO_ORG=$env:ADO_ORG,ADO_PROJECT=$env:ADO_PROJECT,ADO_PAT=$env:ADO_PAT" `
  --memory 1Gi `
  --timeout 600s `
  --max-instances 3
```

**This command:**
- ✅ Builds your Docker image automatically
- ✅ Deploys to Cloud Run
- ✅ Makes it publicly accessible
- ✅ Sets your ADO credentials
- ✅ Allocates 1GB RAM
- ✅ Sets 10-minute timeout
- ✅ Limits to 3 instances max

**Wait 2-3 minutes...**

---

### **Step 5: Get Your Cloud Run URL**

After deployment completes, you'll see:

```
Service [prodreport-refresh] revision [prodreport-refresh-00001-xyz] has been deployed
and is serving 100 percent of traffic.
Service URL: https://prodreport-refresh-xxxxx-uc.a.run.app
```

**Copy this URL!**

---

### **Step 6: Update live_report.html**

Replace the API URL in your code:

```javascript
// Find this line in live_report.html (around line 5530):
const API_BASE_URL = 'http://localhost:5000';

// Change to your Cloud Run URL:
const API_BASE_URL = 'https://prodreport-refresh-xxxxx-uc.a.run.app';
```

---

### **Step 7: Test the Deployment**

```powershell
# Test health check
curl https://prodreport-refresh-xxxxx-uc.a.run.app/api/health

# Should return:
# {"status":"healthy","service":"Report Refresh API","timestamp":"..."}
```

---

### **Step 8: Push Updated HTML to GitHub**

```powershell
git add live_report.html refresh_server.py Dockerfile .dockerignore .gcloudignore
git commit -m "Add Cloud Run deployment support"
git push
```

**Wait 2-3 minutes for GitHub Pages to rebuild**

---

## ✅ **Verify It Works!**

1. Open: https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
2. Click: 🔄 **Refresh from Azure DevOps** button
3. Wait 1-2 minutes
4. Page auto-reloads with fresh ADO data! 🎉

---

## 💰 **Cost Estimate:**

**FREE TIER (Always Free):**
- 2,000,000 requests/month
- 360,000 GB-seconds compute
- 180,000 vCPU-seconds

**Your usage estimate:**
- Refresh 10 times/day = 300/month
- Each refresh ~30-60 seconds
- **You'll stay well within FREE tier!** ✅

---

## 🔧 **Troubleshooting:**

### **Issue: Deployment fails**

```powershell
# Check logs
gcloud run services logs read prodreport-refresh --region us-central1
```

### **Issue: 403 Forbidden**

```powershell
# Make service public
gcloud run services add-iam-policy-binding prodreport-refresh `
  --region us-central1 `
  --member="allUsers" `
  --role="roles/run.invoker"
```

### **Issue: Timeout errors**

```powershell
# Increase timeout to 15 minutes (max)
gcloud run services update prodreport-refresh `
  --region us-central1 `
  --timeout 900s
```

---

## 🔄 **Update Deployment (After Code Changes):**

```powershell
# Simply re-run the deploy command
gcloud run deploy prodreport-refresh `
  --source . `
  --platform managed `
  --region us-central1
```

---

## 🎯 **Summary:**

✅ Files created:
- `Dockerfile` - Container configuration
- `.dockerignore` - Exclude unnecessary files
- `.gcloudignore` - Exclude from upload
- `refresh_server.py` updated for Cloud Run (PORT variable)

✅ Next steps:
1. Install Google Cloud SDK
2. Run `gcloud init`
3. Run deploy command
4. Copy Cloud Run URL
5. Update live_report.html
6. Push to GitHub

**Your "Refresh from Azure DevOps" button will work everywhere!** 🚀
