# 🤖 GitHub Actions Setup Guide

This guide shows you how to configure GitHub Actions to automatically fetch ADO test results and update your live Firebase report.

## ✅ What This Does

- 🔄 **Automatically fetches** test results from Azure DevOps every 4 hours
- 📊 **Generates** production execution reports
- 🔥 **Uploads** data to Firebase Realtime Database
- 🌐 **Updates** your live report at: https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
- 💰 **100% Free** - Uses GitHub Actions free tier

---

## 📋 Setup Steps (10 minutes)

### **Step 1: Get Azure DevOps Personal Access Token (PAT)**

1. Go to: **https://dev.azure.com/accenturecio08/_usersSettings/tokens**
2. Click **"+ New Token"**
3. Configure:
   - **Name**: `GitHub Actions - Test Report`
   - **Organization**: `accenturecio08`
   - **Expiration**: `90 days` (or longer)
   - **Scopes**: Click "Show all scopes" and select:
     - ✅ **Test Management** → **Read**
     - ✅ **Work Items** → **Read**
4. Click **"Create"**
5. **COPY THE TOKEN** - You won't see it again! 🔑

---

### **Step 2: Add Secrets to GitHub Repository**

1. Go to your GitHub repo: **https://github.com/Vishnuramalingam07/Myisp_Tools**

2. Click **"Settings"** (top right)

3. In left sidebar → **"Secrets and variables"** → **"Actions"**

4. Click **"New repository secret"** and add these secrets:

#### **Secret 1: ADO_PAT**
```
Name: ADO_PAT
Value: <paste your ADO Personal Access Token from Step 1>
```

#### **Secret 2: ADO_ORG**
```
Name: ADO_ORG
Value: accenturecio08
```

#### **Secret 3: ADO_PROJECT**
```
Name: ADO_PROJECT
Value: AutomationProcess_29697
```

#### **Secret 4: FIREBASE_DATABASE_URL**
```
Name: FIREBASE_DATABASE_URL
Value: https://myisptools-default-rtdb.firebaseio.com
```

**Result:** You should have 4 secrets configured.

---

### **Step 3: Push Workflow to GitHub**

The workflow file is already created at:
```
.github/workflows/fetch-ado-data.yml
```

Just commit and push it:

```powershell
# Stage the workflow file
git add .github/workflows/fetch-ado-data.yml

# Also add the upload script
git add upload_to_firebase.py

# Commit
git commit -m "Add GitHub Actions workflow for automatic ADO sync"

# Push to GitHub
git push origin main
```

---

### **Step 4: Test the Workflow**

#### **Option A: Manual Trigger (Recommended for testing)**

1. Go to: **https://github.com/Vishnuramalingam07/Myisp_Tools/actions**
2. Click on **"Fetch ADO Test Results and Update Firebase"**
3. Click **"Run workflow"** dropdown
4. Click green **"Run workflow"** button
5. Wait ~2-3 minutes
6. Check the run for success ✅

#### **Option B: Wait for Scheduled Run**

The workflow automatically runs every 4 hours. Next run times:
- 00:00 UTC
- 04:00 UTC
- 08:00 UTC
- 12:00 UTC
- 16:00 UTC
- 20:00 UTC

---

## 🔍 Verify It's Working

### **1. Check GitHub Actions**
Go to: https://github.com/Vishnuramalingam07/Myisp_Tools/actions

You should see:
- ✅ Green checkmark = Success
- ❌ Red X = Failed (check logs)

### **2. Check Firebase Database**
1. Go to: **https://console.firebase.google.com/project/myisptools/database/myisptools-default-rtdb/data**
2. Navigate to: **`prodSanityReport`**
3. You should see:
   - `generated_at` timestamp
   - `uploaded_at` timestamp
   - `statistics` node with test data

### **3. Check Live Report**
Visit: **https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html**

You should see:
- Updated timestamp
- Fresh test results from ADO
- All charts and tables populated

---

## 📊 Workflow Details

### **Schedule**
- Runs **every 4 hours** automatically
- Can be triggered **manually** anytime from GitHub Actions UI

### **What It Does**
```
1. Checkout repository code
2. Setup Python 3.11
3. Install dependencies from requirements.txt
4. Fetch test results from Azure DevOps
   ├── Uses your ADO_PAT secret
   ├── Runs ProdSanity_Report.py
   └── Generates latest_report.json
5. Upload to Firebase
   ├── Uses upload_to_firebase.py
   ├── Connects to Firebase Realtime Database
   └── Updates prodSanityReport node
6. Archive report as artifact (kept for 30 days)
```

### **Runtime**
- Typical run: **2-4 minutes**
- Uses: **~4 minutes** of GitHub Actions quota
- Monthly usage: **~720 minutes** (well within free tier)

---

## 🛠️ Customization

### **Change Schedule**

Edit `.github/workflows/fetch-ado-data.yml`:

```yaml
on:
  schedule:
    - cron: '0 */2 * * *'  # Every 2 hours instead of 4
```

Cron examples:
- `0 * * * *` - Every hour
- `0 */6 * * *` - Every 6 hours
- `0 0 * * *` - Daily at midnight UTC
- `0 9 * * 1-5` - Weekdays at 9am UTC

### **Add Email Notifications**

Add this step to the workflow:

```yaml
- name: Send email notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: GitHub Actions - ADO Sync Failed
    to: your-email@example.com
    from: GitHub Actions
    body: The ADO sync workflow failed. Check logs at ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
```

---

## 🐛 Troubleshooting

### **Error: "Authentication failed"**
- ✅ Check that `ADO_PAT` secret is set correctly
- ✅ Verify PAT hasn't expired (check Azure DevOps)
- ✅ Ensure PAT has correct scopes (Test Management, Work Items)

### **Error: "Firebase upload failed"**
- ✅ Check `FIREBASE_DATABASE_URL` secret is correct
- ✅ Verify Firebase security rules allow writes
- ✅ Check Firebase console for quota limits

### **Error: "Module not found"**
- ✅ Ensure `requirements.txt` is in repo root
- ✅ Check that workflow runs `pip install -r requirements.txt`

### **Workflow doesn't run on schedule**
- ✅ Verify repository is public or has Actions enabled
- ✅ Check if you have recent commits (inactive repos may pause Actions)
- ✅ Review Actions quota on your GitHub account

---

## 📈 Monitoring

### **View Workflow Runs**
https://github.com/Vishnuramalingam07/Myisp_Tools/actions

### **Download Artifacts**
Each run saves the generated report HTML file for 30 days.
Click on any completed run → "Artifacts" → Download

### **Check Logs**
Click on any workflow run → Click on job name → Expand steps to see detailed logs

---

## 🎯 Next Steps

✅ **You're all set!** Your workflow will now:
1. Automatically fetch ADO data every 4 hours
2. Update Firebase with fresh test results
3. Keep your live report always current

### **Optional Enhancements:**
- 📧 Add email notifications on failures
- 📊 Create a dashboard badge showing status
- 🔔 Set up Slack/Teams notifications
- 📝 Add custom post-processing scripts

---

## 💡 Pro Tips

1. **Manual runs**: Use "Run workflow" button for immediate updates
2. **Check logs**: Always review first few runs to ensure everything works
3. **Monitor quota**: GitHub Actions shows usage in repo Settings → Actions
4. **Security**: Never commit PAT tokens to git - always use Secrets
5. **Test locally**: Run scripts locally first before pushing to Actions

---

## 📞 Support

If you encounter issues:
1. Check workflow logs in GitHub Actions
2. Review this guide's troubleshooting section
3. Verify all secrets are configured correctly
4. Test scripts locally to isolate issues

---

**Happy Automating! 🚀**
