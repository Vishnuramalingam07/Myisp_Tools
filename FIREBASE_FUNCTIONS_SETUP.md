# 🔥 Firebase Functions Setup Guide
## Secure Backend for GitHub Actions Workflow Trigger

This guide shows you how to set up Firebase Functions to securely trigger your GitHub Actions workflow from the browser, **without exposing your GitHub token**.

---

## 📋 Architecture

```
GitHub Pages (Public)
  ↓ User clicks "Refresh" button
  ↓
Firebase Cloud Function (Secure)
  ├── GitHub token stored server-side
  ├── Validates request
  └── Triggers GitHub Actions
  ↓
GitHub Actions Workflow
  ├── Fetches ADO data
  ├── Generates report
  └── Updates Firebase Database
  ↓
Live Report Refreshes ✅
```

**Key benefit:** Token never leaves the server, completely secure! 🔒

---

## ⚡ Quick Setup (15 minutes)

### **Step 1: Install Firebase CLI**

```powershell
npm install -g firebase-tools
```

Verify installation:
```powershell
firebase --version
```

---

### **Step 2: Login to Firebase**

```powershell
firebase login
```

This opens your browser to authenticate with Google.

---

### **Step 3: Initialize Firebase Functions**

```powershell
cd C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report

# Initialize Firebase (select existing project)
firebase init functions
```

**During initialization:**
1. Select: **Use an existing project**
2. Choose: **myisptools** (your existing project)
3. Language: **JavaScript**
4. ESLint: **No** (optional)
5. Install dependencies: **Yes**

---

### **Step 4: Deploy the Functions**

The function code is already created in `functions/index.js`.

```powershell
# Navigate to functions directory
cd functions

# Install dependencies
npm install

# Go back to project root
cd ..

# Deploy to Firebase
firebase deploy --only functions
```

**Expected output:**
```
✔  Deploy complete!

Functions:
  ✔  triggerAdoRefresh(us-central1)
  ✔  getWorkflowStatus(us-central1)

Function URL (triggerAdoRefresh):
  https://us-central1-myisptools.cloudfunctions.net/triggerAdoRefresh
```

**Copy this URL!** You'll need it for the next step.

---

### **Step 5: Configure GitHub Token (Secure)**

Store your GitHub token securely in Firebase config:

```powershell
firebase functions:config:set github.token="YOUR_GITHUB_PAT_TOKEN_HERE"
```

**Replace `YOUR_GITHUB_PAT_TOKEN_HERE` with your actual GitHub token!**

Verify it's set:
```powershell
firebase functions:config:get
```

**Redeploy functions** to apply the config:
```powershell
firebase deploy --only functions
```

---

### **Step 6: Update live_report.html**

I'll update your HTML button to call the Firebase Function instead of the local token.

The button will now call:
```
https://us-central1-myisptools.cloudfunctions.net/triggerAdoRefresh
```

---

### **Step 7: Test It!**

1. **Open your live report:**
   ```
   https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
   ```

2. **Click:** 🔄 Refresh from Azure DevOps

3. **Watch:**
   - Progress modal appears
   - Function triggers GitHub Actions
   - Workflow runs (2-3 minutes)
   - Page auto-reloads with fresh data

**Button now works on GitHub Pages!** ✅

---

## 🔍 Verification

### **Test the function directly:**

```powershell
curl -X POST https://us-central1-myisptools.cloudfunctions.net/triggerAdoRefresh
```

**Expected response:**
```json
{
  "success": true,
  "message": "GitHub Actions workflow triggered successfully",
  "workflow": "fetch-ado-data.yml",
  "timestamp": "2026-04-18T..."
}
```

### **Check Firebase logs:**

```powershell
firebase functions:log
```

---

## 💰 Cost

**Firebase Functions Free Tier:**
- ✅ 2 million invocations/month
- ✅ 400,000 GB-seconds compute
- ✅ 200,000 CPU-seconds
- ✅ 5 GB egress/month

**Your usage:**
- Button click = 1 invocation (~500ms runtime)
- Even 1,000 clicks/month = **FREE** ✅

---

## 🔒 Security Benefits

| Before (Client-side token) | After (Firebase Function) |
|----------------------------|---------------------------|
| ❌ Token in browser | ✅ Token on server only |
| ❌ Visible in dev tools | ✅ Never exposed |
| ❌ Public in GitHub repo | ✅ Secure Firebase config |
| ❌ Anyone can misuse | ✅ Controlled access |

---

## 🛠️ Updating the Function

After making changes to `functions/index.js`:

```powershell
firebase deploy --only functions
```

Deploy specific function only:
```powershell
firebase deploy --only functions:triggerAdoRefresh
```

---

## 🐛 Troubleshooting

### **Error: "GitHub token not configured"**

```powershell
# Set the token again
firebase functions:config:set github.token="YOUR_GITHUB_TOKEN"

# Redeploy
firebase deploy --only functions
```

### **Error: "CORS blocked"**

The function already includes CORS headers. If still blocked:
- Check browser console for exact error
- Verify function URL is correct
- Try incognito mode

### **Error: "Permission denied"**

```powershell
# Re-authenticate
firebase login --reauth
```

### **Check function logs:**

```powershell
# Real-time logs
firebase functions:log --only triggerAdoRefresh

# Last 100 lines
firebase functions:log --limit 100
```

---

## 📊 Monitoring

### **View invocations in Firebase Console:**

1. Go to: https://console.firebase.google.com/project/myisptools/functions
2. See: Request count, errors, execution time
3. Click function name for detailed logs

### **Set up alerts:**

Firebase Console → Functions → Alerts
- Alert on errors
- Alert on quota limits
- Email notifications

---

## 🎯 Next Steps

After deployment, your complete setup will be:

1. ✅ **GitHub Pages** - Hosts your live_report.html (public)
2. ✅ **Firebase Functions** - Securely triggers workflows (server-side)
3. ✅ **GitHub Actions** - Fetches ADO data every hour + on-demand
4. ✅ **Firebase Database** - Stores and syncs report data

**All working together, fully automated, and secure!** 🚀

---

## 📝 Commands Reference

```powershell
# Deploy functions
firebase deploy --only functions

# View logs
firebase functions:log

# Get config
firebase functions:config:get

# Set config
firebase functions:config:set github.token="TOKEN"

# Test locally (emulator)
firebase emulators:start --only functions

# Delete a function
firebase functions:delete triggerAdoRefresh
```

---

**Ready to deploy? Let me know once you're ready for Step 6 (updating the HTML)!** 🚀
