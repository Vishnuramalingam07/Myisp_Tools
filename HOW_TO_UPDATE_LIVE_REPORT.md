# 📊 How to Update the Live Report

## 🌐 Live Report URL
**https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html**

Everyone on your team can access this URL to view the latest test execution status.

---

## 🔄 Updating the Live Report (3 Steps)

### **Step 1: Generate New Report**
```powershell
python ProdSanity_Report.py
```

This will:
- ✅ Fetch latest test data from Azure DevOps
- ✅ Generate `live_report.html` (tabbed format)
- ✅ Create `latest_report.json` (data backup)
- ✅ Create timestamped archive file

**Time:** ~2-3 minutes for 1,074 test cases

---

### **Step 2: Commit Changes**
```powershell
git add live_report.html latest_report.json
git commit -m "Update report $(Get-Date -Format 'MMM dd HH:mm')"
```

---

### **Step 3: Push to GitHub**
```powershell
git push
```

**GitHub Actions will automatically deploy to GitHub Pages** (takes 2-3 minutes)

---

## 🎯 Complete Workflow (Copy-Paste)

```powershell
# Generate, commit, and push in one command
python ProdSanity_Report.py; git add live_report.html latest_report.json; git commit -m "Update report $(Get-Date -Format 'HH:mm')"; git push
```

---

## 👥 Who Can Update the Report?

Anyone with:
1. ✅ Access to this repository
2. ✅ Azure DevOps PAT token (set in `.env` file)
3. ✅ Git push permissions

---

## 📋 Report Features

### **6 Tabs Available:**

1. **Prod Sanity Scenarios** - Quick sanity test status
2. **Manual Execution Status** - Manual test results by Lead/Module
3. **Automation Status** - Automation test results
4. **Lead-wise Summary (Manual)** - Aggregated by test lead
5. **Lead-wise Summary (Automation)** - Automation by lead
6. **Bugs** - Active defects grouped by MPOC/Severity

### **Filters:**
- **Lead** - Filter by test lead name
- **Module** - Filter by module name
- Both filters work together (AND logic)

### **Export Options:**
- 📥 **Export to Excel** - Download current view as XLSX
- 🖨️ **Print** - Print-friendly version

---

## 📊 Data Sources

| Data Source | Query/Suite ID | Description |
|-------------|----------------|-------------|
| **Prod Execution** | Suite: 4486314 | Main production test suite |
| **Prod Sanity Scenarios** | Suite: 4486508 | Quick sanity checks |
| **Insprint US Prod Status** | Suite: 4447760 | In-sprint testing |
| **Bugs** | Query: 3e2de1af-6804-4b73-98e8-d3f51beab824 | Active defects |
| **Regression Defects** | Tags: Insprint_Regression, Automation Regression | Created after Feb 12, 2026 |

---

## ⏰ Update Schedule Recommendations

| Frequency | When to Update | Purpose |
|-----------|----------------|---------|
| **Daily** | 9:00 AM, 5:00 PM | Morning status, End of day |
| **After Test Runs** | Immediately | Reflect latest results |
| **Before Meetings** | 15 mins before | Fresh data for discussions |
| **On-Demand** | As needed | When stakeholders request |

---

## 🔒 Security & Access

### **Environment Variables Required:**
```bash
# .env file (DO NOT commit this file!)
ADO_ORGANIZATION=accenturecio08
ADO_PROJECT=AutomationProcess_29697
ADO_PLAN_ID=4444223
ADO_SUITE_ID=4486314
ADO_PAT=your_personal_access_token_here
```

### **Permissions Needed:**
- Azure DevOps: **Read** access to Test Plans
- GitHub: **Write** access to repository
- GitHub Pages: **Enabled** on repository settings

---

## 🐛 Troubleshooting

### **"live_report.html shows old data"**

**Solution:** Hard refresh the page
- Windows/Linux: `Ctrl + Shift + R`
- Mac: `Cmd + Shift + R`
- Or use Incognito/Private mode

---

### **"GitHub Pages not updating"**

**Check GitHub Actions:**
1. Go to: https://github.com/Vishnuramalingam07/Myisp_Tools/actions
2. Look for "pages build and deployment"
3. Wait for green checkmark ✅
4. If failed ❌, check logs

**Wait Time:** 2-3 minutes after push

---

### **"Script fails with authentication error"**

**Check PAT Token:**
```powershell
# Verify .env file exists
Get-Content .env | Select-String "ADO_PAT"

# Test connection
python -c "from ProdSanity_Report import AzureDevOpsClient, ADO_CONFIG; client = AzureDevOpsClient(ADO_CONFIG); client.test_connection()"
```

**Fix:** Regenerate PAT token in Azure DevOps and update `.env`

---

### **"Report shows 0 test cases"**

**Possible Causes:**
1. ❌ Suite ID incorrect in `.env`
2. ❌ No test points in the suite
3. ❌ PAT token lacks permissions

**Fix:** Verify suite IDs in Azure DevOps Test Plans

---

### **"Excel export not working"**

**Check Browser:**
- Works best in Chrome, Edge, Firefox
- Disable popup blockers
- Allow downloads from GitHub Pages

**Alternative:** Copy data from table and paste into Excel

---

## 📱 Sharing the Report

### **Option 1: Share Live URL** ✅ Recommended
```
📊 Latest Test Status: https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

**Advantages:**
- ✅ Always shows latest data (after you push updates)
- ✅ Everyone sees the same version
- ✅ No file attachments needed
- ✅ Works on mobile devices

---

### **Option 2: Share Timestamped File**
```powershell
# Find latest archive
$latest = Get-ChildItem Production_execution_report_*.html | Sort-Object LastWriteTime -Descending | Select-Object -First 1

# Email or share this file
Write-Host "Share this file: $($latest.Name)"
```

**Advantages:**
- ✅ Snapshot at specific time
- ✅ Works offline
- ✅ Can be archived

**Disadvantages:**
- ❌ Gets outdated quickly
- ❌ Need to reshare every update

---

## 📈 Best Practices

### ✅ DO:
- Update report at regular intervals (morning/evening)
- Add meaningful commit messages
- Test connectivity before important meetings
- Archive old timestamped reports monthly
- Share the live URL instead of file attachments
- Hard refresh browser when checking latest updates

### ❌ DON'T:
- Commit `.env` file (contains secrets)
- Push incomplete/test data
- Update during active test execution
- Delete `live_report.html` from repository
- Modify HTML files manually (regenerate instead)

---

## 🔄 Automated Updates (Optional)

### **Windows Task Scheduler**

Create scheduled task to auto-update:

```powershell
# Create update script: update_report.ps1
@"
cd C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report
python ProdSanity_Report.py
git add live_report.html latest_report.json
git commit -m "Auto-update $(Get-Date -Format 'HH:mm')"
git push
"@ | Out-File -FilePath update_report.ps1 -Encoding UTF8

# Run this script via Task Scheduler at 9 AM and 5 PM daily
```

---

### **GitHub Actions (Advanced)**

Create `.github/workflows/auto-update-report.yml`:

```yaml
name: Auto-Update Report
on:
  schedule:
    - cron: '0 3,13 * * *'  # 9 AM and 5 PM IST
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Generate report
        env:
          ADO_PAT: ${{ secrets.ADO_PAT }}
        run: python ProdSanity_Report.py
      - name: Commit and push
        run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add live_report.html latest_report.json
          git commit -m "Auto-update: $(date +'%Y-%m-%d %H:%M')"
          git push
```

---

## 📊 Report Statistics

**Current Data:**
- Total Test Cases: 1,074
- Manual Tests: 57
- Automation Tests: 1,017
- Suites: 53 (Prod Execution)
- Bugs Tracked: 58
- Report Generation Time: ~2-3 minutes

---

## 🆘 Need Help?

### **Quick Commands:**

```powershell
# Check current status
git status

# View last 5 commits
git log --oneline -5

# Discard local changes (use with caution!)
git checkout -- live_report.html

# Pull latest from GitHub
git pull

# View report locally
start live_report.html
```

---

## 📞 Contact

**For issues with:**
- Script errors → Check Azure DevOps connectivity
- GitHub Pages deployment → Check GitHub Actions logs
- Data accuracy → Verify Azure DevOps suite IDs
- Access permissions → Contact repository admin

---

## 📝 Change Log

| Date | Change | Updated By |
|------|--------|------------|
| Apr 17, 2026 | Fixed to generate tabbed format report | GitHub Copilot |
| Apr 17, 2026 | Added live report workflow documentation | GitHub Copilot |

---

## ✅ Summary

**To update the live report, just run:**
```powershell
python ProdSanity_Report.py
git add live_report.html latest_report.json
git commit -m "Update report"
git push
```

**Wait 2-3 minutes, then share:**
```
https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html
```

**That's it!** 🎉
