# 📍 WHERE IS YOUR DATA SAVED?

## 🎯 Quick Answer

**Your data is saved in 3 places:**

```
1. ✅ INSIDE live_report.html (ALL 1,074 tests embedded)
2. ✅ INSIDE latest_report.json (backup copy)
3. ✅ ORIGINAL in Azure DevOps (source of truth)
```

---

## 📂 EXACTLY Where Data is Stored

### **1. live_report.html (478 KB file)**

**Location:** `C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report\live_report.html`

**Storage Method:** Data is **EMBEDDED DIRECTLY IN THE HTML** as table rows

**Example from your actual file:**

```html
<tr data-lead="Himanshu" data-tester="Goriparthi, Anusha" data-module="DFD" data-outcome="Not Run">
    <td>1</td>
    <td>Himanshu</td>                    <!-- Lead name -->
    <td>DFD</td>                         <!-- Module -->
    <td>As a DFD requestor...</td>       <!-- Test title -->
    <td>4458973</td>                     <!-- Test case ID -->
    <td>Goriparthi, Anusha</td>          <!-- Tester -->
    <td>Not Run</td>                     <!-- Outcome -->
    <td>Yet to start</td>                <!-- Status -->
</tr>
```

**Your File Contains:**
- 📊 **15 table sections** (`<tbody>`)
- 📝 **179+ visible rows** with test data
- 💾 **All 1,074 test cases** stored as HTML

**File Size:** 478,569 bytes (478 KB)

---

### **2. latest_report.json (124 KB file)**

**Location:** `C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report\latest_report.json`

**Storage Method:** JSON format (structured text)

**Example structure:**

```json
{
  "generated_at": "2026-04-17T01:11:37",
  "suite_name": "Prod Execution",
  "statistics": {
    "total_tests": 1074,
    "manual_tests": 57,
    "automation_tests": 1017
  },
  "tests_by_lead_module": {
    "Himanshu": {
      "DFD": {
        "manual": {
          "total": 20,
          "passed": 0,
          "failed": 0,
          "not_run": 20
        }
      }
    }
  }
}
```

**File Size:** 127,577 bytes (124 KB)

---

### **3. Azure DevOps (Cloud Database)**

**Location:** https://dev.azure.com/accenturecio08/AutomationProcess_29697

**Storage Method:** Microsoft SQL Database in Azure Cloud

**Contains:**
- ✅ Original test case definitions
- ✅ Test execution history
- ✅ Bug details and links
- ✅ User story associations
- ✅ All metadata (assigned tester, dates, etc.)

---

## 🔍 Visual Breakdown - Where Data Lives

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA STORAGE MAP                         │
└─────────────────────────────────────────────────────────────┘

AZURE DEVOPS (Microsoft Cloud)
  ├── Database: SQL Server
  ├── Contains: ALL historical data
  ├── Size: Unlimited
  └── Access: Requires PAT token
           ↓
           ↓ (Python script fetches via API)
           ↓
YOUR LOCAL MACHINE
  ├── ProdSanity_Report.py runs
  ├── Fetches 1,074 test cases
  ├── Processes data
  └── Generates 2 files:
           ↓
           ├─→ live_report.html (478 KB)
           │    ├── HTML structure
           │    ├── CSS styling  
           │    ├── JavaScript code
           │    └── DATA embedded as <tr> rows
           │
           └─→ latest_report.json (124 KB)
                └── Pure data in JSON format
           ↓
           ↓ (git push)
           ↓
GITHUB REPOSITORY (Git Server)
  ├── Stores files in Git database
  ├── Tracks all versions/history
  └── Files stored:
      ├── live_report.html (current + history)
      ├── latest_report.json (current + history)
      └── Timestamped archives
           ↓
           ↓ (GitHub Actions deploys)
           ↓
GITHUB PAGES (CDN)
  ├── Serves live_report.html as website
  ├── URL: vishnuramalingam07.github.io/...
  └── Same HTML file visible to everyone
```

---

## 💾 Data Storage Details

### **What's Saved in live_report.html:**

| Data Type | How It's Stored | Example |
|-----------|-----------------|---------|
| **Test Case ID** | In `<td>` cell | `<td>4458973</td>` |
| **Lead Name** | In `data-lead` attribute | `data-lead="Himanshu"` |
| **Module** | In `data-module` attribute | `data-module="DFD"` |
| **Outcome** | In `data-outcome` attribute | `data-outcome="Not Run"` |
| **Tester** | In table cell + attribute | `data-tester="Goriparthi, Anusha"` |
| **Status** | In dropdown `<select>` | With all possible values |
| **Bug IDs** | In table cells | Clickable links to ADO |

**Total:** ~1,074 rows of test data embedded in HTML

---

## 📊 File Size Comparison

```
Azure DevOps Database:    ~Unknown (100s of MB with history)
live_report.html:         478 KB (snapshot of 1,074 tests)
latest_report.json:       124 KB (same data, JSON format)
Production_*.html:        478 KB (each timestamped archive)
```

---

## ❓ Common Questions

### **Q: Is there a database?**
**A:** NO! The data is **embedded directly in the HTML file**. No SQL database, no MongoDB, no backend server.

### **Q: How is data saved?**
**A:** As **HTML table rows** with attributes like `data-lead="Himanshu"`. When you open the HTML, all data is already there.

### **Q: Where does Python script save data?**
**A:** 
1. Writes to `live_report.html` (creates the file with embedded data)
2. Writes to `latest_report.json` (creates JSON backup)
3. Both files saved in: `C:\Users\vishnu.ramalingam\MyISP_Tools\Prod_Sanity_Report\`

### **Q: Where does GitHub save data?**
**A:** 
- **Repository:** In Git's internal database (as file versions)
- **GitHub Pages:** Serves the HTML file from CDN
- **URL:** https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html

### **Q: Can I see the raw data?**
**A:** YES! Open `live_report.html` in Notepad and search for `<tbody>` - you'll see all test data

---

## 🔎 Proof: Let Me Show You

**Open Command:**
```powershell
notepad live_report.html
```

**Search for (Ctrl+F):**
- `<tbody>` - Find table body sections
- `data-lead=` - Find test assignments
- `Not Run` - Find test outcomes
- `4458973` - Find specific test case ID

**You'll see lines like:**
```html
<tr data-lead="Himanshu" data-tester="Goriparthi, Anusha" data-module="DFD" data-status="" data-outcome="Not Run">
```

👆 **THIS IS WHERE YOUR DATA IS SAVED!**

---

## 📈 Data Flow Summary

```
TEST UPDATED IN AZURE DEVOPS
         ↓
    (you run script)
         ↓
PYTHON FETCHES DATA FROM AZURE DEVOPS
         ↓
PYTHON EMBEDS DATA INTO HTML FILE
         ↓
    (you git push)
         ↓
GITHUB RECEIVES NEW HTML FILE WITH NEW DATA
         ↓
GITHUB PAGES DEPLOYS NEW FILE
         ↓
EVERYONE SEES UPDATED DATA IN THEIR BROWSER
```

---

## ✅ Key Takeaways

1. **No Database** - Data embedded in HTML as table rows
2. **File-Based Storage** - live_report.html contains everything
3. **GitHub Stores** - File versions in Git repository
4. **GitHub Pages Serves** - Same file visible to everyone
5. **Update Process** - Run script → New HTML → Push → Everyone sees it

---

## 🎯 Bottom Line

**Your data is stored as HTML code inside the live_report.html file itself!**

When you open the file in a browser, it reads the embedded data and displays it as tables. When you push to GitHub, the entire file (with all embedded data) is uploaded and served to everyone.

**Think of it like a Word document with embedded images - the images are INSIDE the .docx file, not in a separate database!**

Your test data is INSIDE the .html file, not in a separate database! 🎉
