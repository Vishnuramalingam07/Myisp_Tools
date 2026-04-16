# 🔧 Local File Viewing Fix

## ❌ The Problem

When you open **`live_report.html`** directly from your file system:

```
file:///C:/Users/vishnu.ramalingam/MyISP_Tools/Prod_Sanity_Report/live_report.html
```

It **keeps loading forever** because:

1. **Browser security** blocks JavaScript from loading `latest_report.json` via `fetch()`
2. **CORS policy** prevents file:// protocol from accessing other local files
3. This is a **security feature** - not a bug!

---

## ✅ Solution 1: Use Standalone Report (Works Locally)

### **Quick Method (One Click):**

Double-click this file:
```
open_local_report.bat
```

**What it does:**
1. ✅ Checks if latest_report.json exists
2. ✅ Creates `standalone_report.html` (data embedded inside)
3. ✅ Opens in your browser automatically

---

### **Manual Method:**

```powershell
# 1. Generate report (if needed)
python ProdSanity_Report.py

# 2. Create standalone version
python create_standalone_report.py

# 3. Open the file
start standalone_report.html
```

**Result:** Works perfectly with `file:///` protocol! ✅

---

## ✅ Solution 2: Use GitHub Pages (Best for Sharing)

**URL:** https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html

**To update:**
```powershell
python ProdSanity_Report.py
git add latest_report.json
git commit -m "Update report"
git push
```

Wait 2-3 minutes, then **hard refresh** browser (`Ctrl+Shift+R`)

---

## ✅ Solution 3: Run Local Web Server

### **Python HTTP Server:**
```powershell
# Start server
python -m http.server 8000

# Open in browser
start http://localhost:8000/live_report.html
```

### **VS Code Live Server:**
1. Install "Live Server" extension
2. Right-click `live_report.html`
3. Select "Open with Live Server"

---

## 📊 Comparison

| Method | Local Viewing | Sharing | Auto-Refresh | Setup Time |
|--------|---------------|---------|--------------|------------|
| **Standalone Report** | ✅ Yes | ❌ No | ❌ No | 10 seconds |
| **GitHub Pages** | ❌ No | ✅ Yes | ✅ Yes | 2-3 minutes |
| **Local Server** | ✅ Yes | ❌ Only on network | ✅ Yes | 30 seconds |
| **Generated HTML** | ✅ Yes | ✅ Can share file | ❌ No | Instant |

---

## 🎯 Recommended Workflows

### **For You (Local Development):**
```powershell
# Option A: Quick view
open_local_report.bat

# Option B: With auto-refresh
python -m http.server 8000
# Then: http://localhost:8000/live_report.html
```

### **For Team (Share URL):**
```powershell
# 1. Generate report
python ProdSanity_Report.py

# 2. Push to GitHub
git add latest_report.json
git commit -m "Update $(Get-Date -Format HH:mm)"
git push

# 3. Share link (wait 2-3 mins)
# https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

---

## 🐛 Troubleshooting

### **"standalone_report.html still loading"**

**Check console (F12):**
- Should see: `✅ Loading embedded data...`
- Should NOT see: `📡 Fetching: ...`

**If still stuck:**
```powershell
# Regenerate with fresh data
python ProdSanity_Report.py
python create_standalone_report.py
```

### **"GitHub Pages shows old data"**

**Hard refresh:**
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`

**Or incognito mode:**
- Windows: `Ctrl + Shift + N`
- Mac: `Cmd + Shift + N`

---

## 📝 Files Explained

| File | Purpose | Opens Locally? |
|------|---------|----------------|
| **live_report.html** | For GitHub Pages (fetches JSON) | ❌ No - CORS blocked |
| **standalone_report.html** | Generated - data embedded | ✅ Yes - works offline |
| **Production_execution_report_*.html** | Generated - traditional format | ✅ Yes - no dependencies |
| **latest_report.json** | Data file (for GitHub Pages) | N/A - not HTML |

---

## 🚀 Quick Start

**Most common scenario:**

```powershell
# Generate report + open locally
python ProdSanity_Report.py
python create_standalone_report.py
start standalone_report.html
```

**Done!** Your browser opens with working dashboard. 🎉

---

## 💡 Why Two Versions?

### **live_report.html (GitHub Pages)**
- ✅ Auto-refreshes every 30 seconds
- ✅ Multiple users see same data
- ✅ Share one URL to everyone
- ❌ Needs web server (HTTP/HTTPS)

### **standalone_report.html (Local)**
- ✅ Works with file:// protocol
- ✅ No server needed
- ✅ Works offline
- ❌ Data frozen at generation time
- ❌ Can't auto-refresh

---

## ✅ Summary

**Problem:** Browser security blocks `file:///` access to JSON  
**Solution:** Use `standalone_report.html` for local viewing  
**Command:** `python create_standalone_report.py` or `open_local_report.bat`  

**For live updates:** Use GitHub Pages instead:  
🔗 https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
