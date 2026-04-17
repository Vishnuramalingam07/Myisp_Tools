# 📊 Google Sheets API Setup Guide

Complete step-by-step guide to enable collaborative editing using Google Sheets.

---

## 🎯 Overview

This setup allows your **live_report.html** on GitHub Pages to sync data to Google Sheets, enabling real-time collaboration without needing a backend server!

**Architecture:**
```
GitHub Pages (live_report.html) 
    ↓ JavaScript
Google Sheets API
    ↓ Read/Write
Google Spreadsheet (shared data storage)
```

---

## 📋 Prerequisites

- Google Account
- GitHub Pages site (already set up)
- 15 minutes for initial setup

---

## 🚀 Step-by-Step Setup

### **STEP 1: Create Google Cloud Project**

1. Go to **[Google Cloud Console](https://console.cloud.google.com/)**

2. Click **"Select a project"** → **"New Project"**

3. Enter project details:
   - **Project Name**: `Live Report Collaboration` (or your choice)
   - **Organization**: Leave as default or select your org
   - Click **"Create"**

4. Wait for the project to be created (takes ~30 seconds)

5. Make sure the new project is selected in the dropdown at the top

---

### **STEP 2: Enable Google Sheets API**

1. In the Google Cloud Console, go to **"APIs & Services"** → **"Library"**
   - Or directly: https://console.cloud.google.com/apis/library

2. Search for **"Google Sheets API"**

3. Click on **"Google Sheets API"** from the results

4. Click the **"Enable"** button

5. Wait for activation (~15 seconds)

---

### **STEP 3: Create API Credentials**

1. Go to **"APIs & Services"** → **"Credentials"**
   - Or directly: https://console.cloud.google.com/apis/credentials

2. Click **"+ CREATE CREDENTIALS"** → **"API key"**

3. Your API key will be created and displayed:
   ```
   AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

4. **⚠️ IMPORTANT**: Click **"RESTRICT KEY"** to secure it

5. In the API restrictions section:
   - Select **"Restrict key"**
   - Check **"Google Sheets API"** only
   - Click **"Save"**

6. **Copy your API key** - you'll need it in Step 5

---

### **STEP 4: Create the Google Spreadsheet**

1. Go to **[Google Sheets](https://sheets.google.com/)**

2. Click **"+ Blank"** to create a new spreadsheet

3. Name it: **"Live Report Collaborative Data"**

4. Create the following sheets (tabs) by clicking **+** at the bottom:
   - `Summary`
   - `Execution`
   - `BugAnalysis`
   - `Coverage`
   - `Regressions`
   - `TestCases`

5. **Important - Make it Public for Editing:**
   - Click **"Share"** button (top right)
   - Click **"Change to anyone with the link"**
   - Change permission from "Viewer" to **"Editor"**
   - Click **"Done"**
   
   **⚠️ Security Note**: This makes the sheet publicly editable. Anyone with the link can edit it. For production use, consider using OAuth 2.0 authentication instead.

6. **Copy the Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_SPREADSHEET_ID_HERE/edit
                                         ^^^^^^^^^^^^^^^^^^^^^^^^
   ```
   Example: `1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms`

---

### **STEP 5: Configure Your Project**

1. Open **`google-sheets-config.js`** in your project

2. Replace the placeholder values:

```javascript
const GOOGLE_SHEETS_CONFIG = {
    // STEP 1: Replace with your Google Sheets API Key from Step 3
    API_KEY: 'AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    
    // STEP 2: Replace with your Spreadsheet ID from Step 4
    SPREADSHEET_ID: '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms',
    
    // ... rest of config stays the same
};
```

3. **Save the file**

---

### **STEP 6: Test Locally**

1. Open **live_report.html** in your browser (double-click or serve locally)

2. Look for the sync status indicator in the top-right:
   - 🟢 **Green** = "Google Sheets Connected" ✅
   - ⚪ **Gray** = "Not Configured" ❌

3. Try saving some data:
   - Fill in some test values
   - Click **"💾 Save"**
   - You should see: **"✓ Synced to Google Sheets"**

4. **Verify in Google Sheets:**
   - Open your spreadsheet
   - Go to the **"Summary"** tab
   - You should see your data appear!

5. **Test Multi-User Sync:**
   - Open the same HTML file in another browser/incognito window
   - Make a change and save
   - Wait 5 seconds for polling to refresh
   - The other window should show the update notification

---

### **STEP 7: Deploy to GitHub Pages**

1. **Commit your changes:**
```bash
git add google-sheets-config.js live_report.html GOOGLE_SHEETS_SETUP.md
git commit -m "Add Google Sheets API integration for collaborative editing"
git push origin main
```

2. **Access your live site:**
   - Go to: `https://YOUR_USERNAME.github.io/YOUR_REPO/live_report.html`
   - Example: `https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html`

3. **Test collaborative editing:**
   - Open the URL on your phone/tablet or share with a colleague
   - Both users make changes
   - Changes sync within ~5 seconds!

---

## ✅ Verification Checklist

- [ ] Google Cloud project created
- [ ] Google Sheets API enabled
- [ ] API key created and restricted
- [ ] Spreadsheet created with correct sheet names
- [ ] Spreadsheet set to public "Editor" access
- [ ] API_KEY configured in google-sheets-config.js
- [ ] SPREADSHEET_ID configured in google-sheets-config.js
- [ ] Local test shows green "Google Sheets Connected" status
- [ ] Data saves successfully to Google Sheets
- [ ] Deployed to GitHub Pages
- [ ] Multi-user sync works

---

## 🔧 Troubleshooting

### ❌ "Not Configured" Status

**Problem**: Gray indicator shows "Not configured"

**Solutions**:
1. Check that you replaced `YOUR_API_KEY_HERE` in google-sheets-config.js
2. Check that you replaced `YOUR_SPREADSHEET_ID_HERE` in google-sheets-config.js
3. Clear browser cache and reload

### ❌ "Google Sheets Error - Check Config"

**Problem**: Red indicator shows error

**Solutions**:
1. **API Key Issues:**
   - Verify the API key is correct (no extra spaces)
   - Check that Google Sheets API is enabled in Google Cloud Console
   - Verify API key restrictions allow Google Sheets API

2. **Spreadsheet Access:**
   - Make sure spreadsheet is set to "Anyone with the link" can **edit** (not just view)
   - Verify the Spreadsheet ID is correct

3. **Sheet Names:**
   - Make sure the sheet tabs are named exactly: `Summary`, `Execution`, `BugAnalysis`, `Coverage`, `Regressions`, `TestCases`
   - Names are case-sensitive!

### ❌ "Saved Locally" but Not to Sheets

**Problem**: Button shows "Saved Locally" instead of "Synced to Google Sheets"

**Solutions**:
1. Open browser console (F12) to see error messages
2. Check for CORS errors (should not happen with Google Sheets API)
3. Verify API quota hasn't been exceeded (check Google Cloud Console)

### ❌ Data Not Updating for Other Users

**Problem**: Changes don't sync to other users

**Solutions**:
1. Wait 5 seconds - polling interval
2. Check that both users are connected (green indicator)
3. Try manually refreshing the page
4. Verify spreadsheet has "Editor" permissions

### 📊 API Quota Limits

Google Sheets API has usage limits:
- **Free tier**: 100 requests per 100 seconds per user
- **Daily limit**: 500 requests per project per day

For your use case with 5-second polling:
- Each user = 12 requests/minute
- 5 users continuously using = 60 requests/minute = ~3600/hour

**If you hit limits:**
1. Increase polling interval to 10 seconds: `setInterval(pollForUpdates, 10000)`
2. Request quota increase in Google Cloud Console
3. Consider upgrading to paid tier

---

## 🔒 Security Considerations

### ⚠️ Current Setup (Public Editing)

- Spreadsheet is publicly editable by anyone with the link
- API key is exposed in client-side JavaScript
- Suitable for internal teams or low-security data

### 🔐 For Production/Sensitive Data

Consider implementing OAuth 2.0:
1. Users sign in with Google Account
2. Data access controlled per-user
3. API key not exposed in client code

**Need OAuth setup?** Let me know and I can create that configuration!

---

## 📈 Benefits of This Approach

✅ **No Server Required** - Works entirely on GitHub Pages (static hosting)  
✅ **Free** - Google Sheets API free tier is generous  
✅ **Real-time** - Changes sync within 5 seconds  
✅ **Familiar Interface** - Team can also edit directly in Google Sheets  
✅ **Backup** - All data is in Google Sheets (downloadable as Excel)  
✅ **Version History** - Google Sheets tracks all changes  
✅ **Scalable** - Handles multiple concurrent users  

---

## 🎓 How It Works

1. **User Opens Page** → JavaScript loads google-sheets-config.js
2. **Page Loads** → Fetches latest data from Google Sheets
3. **User Edits** → Saves to localStorage + Google Sheets simultaneously
4. **Auto-Polling** → Every 5 seconds, checks for updates from other users
5. **Update Detected** → Notifies user or silently updates inactive tabs
6. **Everyone Synced** → All users see the latest data

---

## 📚 Additional Resources

- [Google Sheets API Documentation](https://developers.google.com/sheets/api)
- [Google Cloud Console](https://console.cloud.google.com/)
- [API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)
- [Sheets API Quotas & Limits](https://developers.google.com/sheets/api/limits)

---

## 💡 Next Steps

After setup is complete:
1. Share the live URL with your team
2. Monitor the Google Spreadsheet for data sync
3. Consider adding more sheets/tabs as needed
4. Set up notifications for important changes
5. Export data periodically as backup

---

## 🆘 Still Need Help?

If you encounter issues:
1. Check browser console for error messages (F12)
2. Verify all 6 sheet tabs exist with exact names
3. Test API key in Google's [API Explorer](https://developers.google.com/apis-explorer)
4. Review the Google Cloud Console error logs

---

**✨ Setup Complete! Your collaborative live report is ready!** ✨
