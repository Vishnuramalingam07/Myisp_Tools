# 📁 JSON-Based Live Report (No Backend Required!)

## 🎯 Overview

**Simple architecture:** Excel + JSON updates via Git push = Live Dashboard

```
 Run Report (Local)          GitHub (FREE)           Users (Anywhere)
┌────────────────┐          ┌──────────────┐        ┌──────────────┐
│ProdSanity_     │          │              │        │              │
│Report.py       │──────►   │latest_report │  ◄────│ Live HTML    │
│                │  Push    │ .json        │  Read │ Dashboard    │
│ - Excel Report │          │              │       │ Auto-refresh │
│ - JSON Export  │          │              │       │              │
└────────────────┘          └──────────────┘        └──────────────┘
```

## ✅ Advantages

✅ **No backend hosting needed** - No PostgreSQL, No Flask API  
✅ **Zero cost** - Everything on GitHub (free)  
✅ **Simple workflow** - Just run script + git push  
✅ **Auto-refresh** - JavaScript reloads JSON every 30 seconds  
✅ **Excel + HTML + JSON** - All formats generated  
✅ **Shareable link** - Anyone can view: `https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html`  

## ⚠️ Limitations

⚠️ **Not instant** - Requires manual git push after report generation  
⚠️ **GitHub caching** - May take 1-5 minutes for updates to appear  
⚠️ **Not real-time** - Good for hourly/daily updates, not second-by-second  

---

## 🚀 How It Works

### **Step 1: Generate Report**

Run the Python script as usual:

```powershell
cd "C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report"
python ProdSanity_Report.py
```

**Output:**
- ✅ `Production_execution_report_20260417_120000.html` (HTML report for viewing)
- ✅ `Production_execution_report_20260417_120000.xlsx` (Excel report - if implemented)
- ✅ `latest_report.json` **(NEW!)** - Data for live dashboard

### **Step 2: Push JSON to GitHub**

```powershell
git add latest_report.json
git commit -m "Update production report data"
git push
```

> **Note:** Only push `latest_report.json` - HTML/Excel reports are optional

### **Step 3: Users Access Live Dashboard**

**URL:** https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html

- Auto-refreshes every 30 seconds
- Shows latest stats from JSON file
- Works on any device (desktop, tablet, mobile)
- No login required

---

## 📁 What's in latest_report.json?

```json
{
  "generated_at": "2026-04-17T12:00:00",
  "timestamp_display": "April 17, 2026 at 12:00:00",
  "suite_name": "Prod Execution",
  "statistics": {
    "total_tests": 1074,
    "manual_tests": 840,
    "automation_tests": 234,
    "outcomes": {
      "Passed": 850,
      "Failed": 120,
      "Blocked": 50,
      "Not Run": 54
    },
    "grand_totals": {
      "manual": {
        "total": 840,
        "passed": 650,
        "failed": 100,
        "pass_percentage": 86.7,
        "execution_percentage": 89.3
      },
      "automation": {
        "total": 234,
        "passed": 200,
        "failed": 20,
        "pass_percentage": 90.9,
        "execution_percentage": 94.0
      }
    }
  },
  "bugs": {
    "total_from_query": 145,
    "filtered_count": 98,
    "bugs_list": [...]
  },
  "tests_by_lead_module": {
    "Selva Kumar": {
      "Catalog": {
        "manual": {...},
        "automation": {...}
      }
    }
  }
}
```

**File Size:** ~50-200 KB (small, fast to load)

---

## 🔄 Daily Workflow

### **Morning Report:**

```powershell
# 1. Generate report
python ProdSanity_Report.py

# 2. Push to GitHub
git add latest_report.json
git commit -m "Morning report - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push
```

### **After Each Test Run:**

```powershell
# Quick update
python ProdSanity_Report.py; git add latest_report.json; git commit -m "Update $(Get-Date -Format HH:mm)"; git push
```

### **One-Liner (PowerShell):**

```powershell
python ProdSanity_Report.py; if($?) { git add latest_report.json; git commit -m "Report update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"; git push }
```

---

## 🌐 Access URLs

| Item | URL |
|------|-----|
| **Live Dashboard** | https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html |
| **JSON Data (relative)** | `/latest_report.json` (served by GitHub Pages) |
| **JSON Data (GitHub raw)** | https://raw.githubusercontent.com/Vishnuramalingam07/Myisp_Tools/main/latest_report.json |
| **GitHub Repo** | https://github.com/Vishnuramalingam07/Myisp_Tools |
| **Static Reports** | https://Vishnuramalingam07.github.io/Myisp_Tools/ |

---

## 🎛️ Live Dashboard Features

<table>
<tr>
<td width="50%">

**Auto-Refresh Options:**
- ⚡ 30 seconds (default)
- ⏱️ 1 minute
- 🕐 5 minutes
- ✋ Manual refresh

</td>
<td width="50%">

**Display Features:**
- 📊 Total test count
- ✏️ Manual test stats
- 🤖 Automation stats
- 🐛 Bug counts
- 📈 Outcome breakdown

</td>
</tr>
</table>

**Controls:**
- 🔄 **Refresh Now** - Force immediate update
- 📥 **Export JSON** - Download current data
- 🟢 **Live Indicator** - Shows connection status

---

## 🐛 Troubleshooting

### **Dashboard shows "OFFLINE"**

**Causes:**
1. `latest_report.json` not pushed to GitHub yet
2. GitHub caching (wait 1-5 minutes)
3. Browser cache issue

**Fix:**
```powershell
# Verify JSON exists in repo
git ls-files | Select-String "latest_report.json"

# Push if missing
git add latest_report.json
git commit -m "Add latest report"
git push

# Clear browser cache: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
```

### **Dashboard shows old data**

**Fix:**
```powershell
# 1. Generate fresh report
python ProdSanity_Report.py

# 2. Verify JSON is different
git status

# 3. Push new data
git add latest_report.json
git commit -m "Fresh data"
git push

# 4. Wait 1-2 minutes for GitHub CDN to update
# 5. Hard refresh browser: Ctrl+Shift+R
```

### **JSON file too large (>1MB)**

**Current size:** ~50-200 KB ✅

If it grows too large, edit `ProdSanity_Report.py`:

```python
# Line in export_to_json method:
"test_details": self.test_data[:50]  # Reduce from 100 to 50
```

### **Updates take too long to appear**

**GitHub caching:**
- First load: Instant
- Subsequent updates: 1-5 minute delay (GitHub CDN caching)
- Cannot be avoided with free GitHub Pages

**Options:**
1. Wait 2-5 minutes after git push
2. Use manual refresh instead of auto-refresh
3. Deploy backend (Railway/Render) for instant updates

---

## 📊 Comparison: JSON vs Backend

| Feature | JSON (GitHub) | Backend (Railway) |
|---------|---------------|-------------------|
| **Setup Time** | 5 minutes ✅ | 30-60 minutes |
| **Hosting Cost** | $0 ✅ | $0-20/month |
| **Update Speed** | 1-5 min delay ⚠️ | Instant ✅ |
| **Workflow** | Generate + Push | Generate only ✅ |
| **Maintenance** | None ✅ | Server monitoring |
| **Max File Size** | 100 MB ✅ | Unlimited ✅ |

**Recommendation:**
- **Use JSON for:** Daily/hourly reports, team dashboards, demos
- **Use Backend for:** Real-time monitoring, production systems, customer-facing dashboards

---

## 🎉 Summary

**What changed:**

| Before | After |
|--------|-------|
| ❌ Required PostgreSQL | ✅ Just JSON file |
| ❌ Required Flask API | ✅ Static HTML + JavaScript |
| ❌ Backend deployment | ✅ GitHub Pages only |
| ❌ Complex setup | ✅ Simple git push |
| 💰 $20/month cost | 💰 $0/month |

**Your workflow now:**

```powershell
# Run report (generates HTML, Excel, JSON)
python ProdSanity_Report.py

# Push JSON to GitHub
git add latest_report.json
git commit -m "Update report"
git push

# Share link (data auto-updates in browser)
https://Vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

✅ **Simple, free, and works!**
