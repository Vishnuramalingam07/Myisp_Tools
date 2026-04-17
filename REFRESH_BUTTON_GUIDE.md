# 🔄 Azure DevOps Refresh Button - Setup Guide

## ✅ **What Was Added**

A **"Refresh from Azure DevOps"** button that:
- ✅ Fetches fresh test data from Azure DevOps
- ✅ Regenerates the HTML with latest data
- ✅ Shows real-time progress (Step 1/3, 2/3, 3/3)
- ✅ Auto-reloads the page when complete
- ✅ Preserves Firebase user edits (they merge automatically)

---

## 🚀 **How to Use**

### **Step 1: Install Dependencies**

```bash
pip install flask flask-cors
```

*(Already in requirements.txt)*

---

### **Step 2: Start the API Server**

Open a **new terminal** and run:

```bash
cd C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report
python refresh_server.py
```

**You should see:**
```
🚀 REPORT REFRESH API SERVER
   • API Server: http://localhost:5000
   • Live Report: http://localhost:5000/
```

**Keep this terminal running!**

---

### **Step 3: Open the Report**

**Option A: Via API Server (Recommended)**
```
http://localhost:5000/
```

**Option B: GitHub Pages**
```
https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```
*(Note: GitHub Pages needs manual Python run + git push)*

---

### **Step 4: Click the Refresh Button**

1. **Click:** 🔄 **"Refresh from Azure DevOps"** button
2. **Wait:** Progress modal shows steps (1-2 minutes)
   - Step 1/3: Fetching test data from Azure DevOps...
   - Step 2/3: Processing test cases and bugs...
   - Step 3/3: Generating HTML report...
3. **Auto-reload:** Page refreshes with new data
4. **Firebase merge:** Your saved edits remain intact ✅

---

## 📊 **What Gets Updated**

### ✅ **Refreshed from Azure DevOps:**
- Test case list (new/removed tests)
- Test outcomes (Pass/Fail/Blocked)
- Bug lists and states
- User stories and requirements
- Module assignments

### ✅ **Preserved from Firebase:**
- User status changes (e.g., "Blocked" → "Working fine")
- Comments added by users
- Any manual edits made through the web UI

---

## 🎯 **Workflow Example**

### **Daily Morning Update:**

```bash
# Terminal 1: Start API server (once)
python refresh_server.py

# Browser: Open report
http://localhost:5000/

# Click "Refresh from Azure DevOps" button
# Wait 1-2 minutes → Page auto-reloads with fresh ADO data
# Your team's Firebase edits are still there!
```

---

## 🔧 **Troubleshooting**

### **Problem: Button does nothing**

**Check:**
```bash
# Is API server running?
curl http://localhost:5000/api/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Report Refresh API"
}
```

**Solution:** Start the server:
```bash
python refresh_server.py
```

---

### **Problem: "Failed to refresh data"**

**Check console (F12):**
- ❌ `Failed to fetch` → API server not running
- ❌ `Connection refused` → Wrong port
- ❌ `500 error` → Python script error

**Solution:**
1. Check API server terminal for errors
2. Verify ADO credentials in `.env` file
3. Check `ADO_PAT` token is valid

---

### **Problem: Refresh hangs / times out**

**Possible causes:**
- Azure DevOps API is slow (large test suites)
- Network issues
- PAT token expired

**Solution:**
- Wait up to 2 minutes
- Check API server terminal for progress
- Refresh will timeout and show error after 2 minutes

---

## 🌐 **GitHub Pages Workflow**

**If using GitHub Pages (without local server):**

### **Manual Refresh Process:**

```bash
# 1. Run Python script locally
python ProdSanity_Report.py

# 2. Commit and push
git add live_report.html latest_report.json
git commit -m "Update ADO data $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push

# 3. Wait 2-3 minutes for GitHub Pages to rebuild
# 4. Refresh browser
https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

*(Note: Button won't work on GitHub Pages without backend server)*

---

## 📝 **API Endpoints**

### **Health Check**
```bash
GET http://localhost:5000/api/health
```

### **Trigger Refresh**
```bash
POST http://localhost:5000/api/refresh
```

### **Check Status**
```bash
GET http://localhost:5000/api/status
```
Returns: `running`, `last_status`, `output`, `last_error`

---

## 💡 **Best Practices**

### **Daily Workflow:**

1. **Morning:** Start API server once
   ```bash
   python refresh_server.py
   ```

2. **Throughout Day:** Team edits via browser
   - Changes save to Firebase automatically
   - No need to refresh from ADO constantly

3. **When Needed:** Click refresh button
   - New test cases added in ADO
   - Bug states changed in ADO
   - Major ADO updates

4. **Before Meetings:** Refresh for latest counts

---

## 🔐 **Security Notes**

- API server runs on **localhost:5000** (local machine only)
- Not exposed to internet (safe for internal use)
- Firebase already has security rules configured
- ADO PAT token stored in `.env` (not committed to git)

---

## ✅ **Summary**

**What you can do now:**
- ✅ **One-click refresh** from Azure DevOps
- ✅ **Real-time progress** updates
- ✅ **Auto-merge** with Firebase edits
- ✅ **No manual Python runs** needed
- ✅ **Team collaboration** continues seamlessly

**The button makes it easy to sync ADO data without losing collaborative edits!** 🎉
