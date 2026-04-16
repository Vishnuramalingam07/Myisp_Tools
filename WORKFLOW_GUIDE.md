# 📊 Production Sanity Report - Complete Workflow Guide

## 🎯 Overview

This system generates Azure DevOps test execution reports in multiple formats:

1. **Dashboard HTML Report** - Beautiful snapshot with statistics cards
2. **Live Report (GitHub Pages)** - Auto-refreshing online dashboard
3. **Standalone Report** - Works offline with embedded data
4. **JSON Data File** - For programmatic access

---

## 🚀 Quick Start

### **Generate Reports:**

```powershell
python ProdSanity_Report.py
```

**Output:**
- `Production_execution_report_YYYYMMDD_HHMMSS.html` - Timestamped dashboard snapshot
- `standalone_report.html` - Embedded data (works with `file://`)
- `latest_report.json` - Data file (124 KB)
- `live_report.html` - Template (already exists, NOT overwritten)

---

## 📁 File Types Explained

### 1. **Production_execution_report_YYYYMMDD_HHMMSS.html**
- ✅ Dashboard-style HTML with all data embedded
- ✅ Opens directly in browser (double-click)
- ✅ No dependencies required
- ✅ Timestamped for archival
- **Use Case:** Quick view, email to team, archive

### 2. **standalone_report.html**
- ✅ Dashboard with embedded JSON data
- ✅ Works with `file://` protocol
- ✅ No network required
- ✅ Updates with each run
- **Use Case:** Local viewing, offline access

### 3. **latest_report.json**
- ✅ Raw test data (124 KB)
- ✅ Powers the live dashboard
- ✅ Used by GitHub Pages
- **Use Case:** Live dashboard data source

### 4. **live_report.html**
- ✅ Template with auto-refresh (30s/60s/5min)
- ✅ Fetches data from `latest_report.json`
- ✅ Hosted on GitHub Pages
- ❌ Does NOT work locally (`file://` blocked by CORS)
- **Use Case:** Shareable live URL for team

---

## 🌐 GitHub Pages Deployment

### **Update Live Dashboard:**

```powershell
# 1. Generate reports
python ProdSanity_Report.py

# 2. Commit and push JSON data
git add latest_report.json
git commit -m "Update report data $(Get-Date -Format 'HH:mm')"
git push

# 3. Wait 2-3 minutes for GitHub Actions to deploy

# 4. View live dashboard
start https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

**Auto-Refresh:** Dashboard updates every 30 seconds automatically

**Cache Issues:** Use `Ctrl+Shift+R` to force refresh

---

## 💻 Local Viewing Options

### **Option A: Open Timestamped Report (Recommended)**
```powershell
# Find latest report
$latest = Get-ChildItem Production_execution_report_*.html | Sort-Object LastWriteTime -Descending | Select-Object -First 1
start $latest.Name
```
✅ Works immediately  
✅ Static snapshot  
✅ No dependencies  

### **Option B: Open Standalone Report**
```powershell
start standalone_report.html
```
✅ Works with `file://` protocol  
✅ Updated with each run  
❌ Requires `latest_report.json` in same directory  

### **Option C: Use Batch Script**
```powershell
.\open_local_report.bat
```
✅ One-click solution  
✅ Generates if missing  
✅ Opens automatically  

### **Option D: Local Web Server (For live_report.html)**
```powershell
# Python HTTP Server
python -m http.server 8000

# Open in browser
start http://localhost:8000/live_report.html
```
✅ Auto-refresh works  
✅ Mirrors GitHub Pages behavior  
❌ Requires server running  

---

## 📊 Report Comparison

| Feature | Timestamped HTML | Standalone HTML | Live Report (GitHub) |
|---------|------------------|-----------------|----------------------|
| **File Name** | `Production_execution_report_*.html` | `standalone_report.html` | `live_report.html` |
| **Opens Locally** | ✅ Yes | ✅ Yes | ❌ No (CORS blocked) |
| **Auto-Refresh** | ❌ No | ❌ No | ✅ Yes (30s/60s/5min) |
| **Data Source** | Embedded | Embedded | Fetches JSON |
| **Shareable** | ✅ Yes (send file) | ✅ Yes (send file) | ✅ Yes (URL) |
| **Updates** | Never (snapshot) | Each generation | Real-time |
| **Best For** | Archive, email | Local viewing | Team sharing |

---

## 🔧 Workflows

### **Daily Status Report (Team Share)**
```powershell
# Morning update
python ProdSanity_Report.py
git add latest_report.json
git commit -m "Morning status $(Get-Date -Format 'dd/MM HH:mm')"
git push

# Share link in Slack/Teams
echo "📊 Latest report: https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html"
```

### **Quick Check (Solo)**
```powershell
# Generate and open
python ProdSanity_Report.py

# Open latest report
$latest = Get-ChildItem Production_execution_report_*.html | Sort-Object LastWriteTime -Descending | Select-Object -First 1
start $latest.Name
```

### **Offline/Traveling**
```powershell
# Generate before going offline
python ProdSanity_Report.py

# Later: open standalone
start standalone_report.html
```

### **Archive Monthly Reports**
```powershell
# Create archive folder
New-Item -Type Directory -Path "Archive\April_2026" -Force

# Move old reports
Move-Item Production_execution_report_202604*.html Archive\April_2026\
```

---

## 🐛 Troubleshooting

### **"live_report.html keeps loading locally"**
**Problem:** Browser blocks `fetch()` on `file://` protocol (CORS security)

**Solution:** Use `standalone_report.html` instead OR run local server:
```powershell
python -m http.server 8000
start http://localhost:8000/live_report.html
```

### **"GitHub Pages shows old data"**
**Problem:** Browser cache

**Solution:** Hard refresh with `Ctrl+Shift+R` or incognito mode

### **"standalone_report.html is blank"**
**Problem:** Missing `latest_report.json`

**Solution:** Generate reports first:
```powershell
python ProdSanity_Report.py
```

### **"Dashboard looks broken"**
**Problem:** Mixed content or file corruption

**Solution:** Regenerate all files:
```powershell
# Clean old files
Remove-Item standalone_report.html -ErrorAction SilentlyContinue

# Regenerate
python ProdSanity_Report.py
```

---

## 📦 File Dependencies

```
ProdSanity_Report.py            # Main generator script
├── Generates: Production_execution_report_*.html  # Timestamped snapshot
├── Generates: latest_report.json                  # Data file (124 KB)
└── Generates: standalone_report.html              # Embedded version

create_standalone_report.py     # Standalone generator
├── Reads: latest_report.json
├── Reads: live_report.html (template)
└── Generates: standalone_report.html

live_report.html                # GitHub Pages template (DO NOT DELETE)
├── Fetches: latest_report.json
└── Deployed to: GitHub Pages

open_local_report.bat           # Quick access script
├── Checks: latest_report.json
├── Runs: ProdSanity_Report.py (if needed)
└── Opens: standalone_report.html
```

---

## 🔐 Security Notes

- **PAT Token:** Stored in `.env` file (gitignored)
- **No Credentials in Reports:** All HTML files are safe to share
- **JSON Data:** Public on GitHub Pages (contains test data only)

---

## 📝 Configuration

Edit `.env` file for settings:
```bash
ADO_ORGANIZATION=accenturecio08
ADO_PROJECT=AutomationProcess_29697
ADO_PLAN_ID=4444223
ADO_SUITE_ID=4486314
ADO_PAT=your_personal_access_token_here
```

---

## 🎨 Customization

### **Change Auto-Refresh Interval (live_report.html)**
Edit line in `live_report.html`:
```javascript
let refreshInterval = 30; // Change to 60, 120, 300, etc.
```

### **Disable Auto-Refresh**
Remove these lines from `live_report.html`:
```javascript
startAutoRefresh();
```

---

## 💡 Tips & Best Practices

1. **Keep Timestamped Reports:** Archive monthly for history
2. **Use Batch Script:** Double-click `open_local_report.bat` for quick access
3. **Share GitHub Pages URL:** Don't email HTML files, share the live link
4. **Check Git Status:** Ensure `latest_report.json` is committed after updates
5. **Hard Refresh GitHub Pages:** Use `Ctrl+Shift+R` to see latest data

---

## 🔗 Quick Links

- **Live Dashboard:** https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
- **GitHub Repository:** https://github.com/Vishnuramalingam07/Myisp_Tools
- **Azure DevOps:** https://dev.azure.com/accenturecio08/AutomationProcess_29697

---

## ✅ Summary

| **Need** | **Command** | **Output** |
|----------|-------------|------------|
| Generate all reports | `python ProdSanity_Report.py` | 3 files |
| Open locally (quick) | Double-click timestamped HTML | Opens in browser |
| Open locally (latest) | `start standalone_report.html` | Opens latest |
| Update live dashboard | `git add latest_report.json; git commit; git push` | GitHub Pages updated |
| Share with team | Send live dashboard URL | Everyone sees same data |

---

**Last Updated:** April 17, 2026  
**Version:** 2.0 (Dashboard-style with multiple output formats)
