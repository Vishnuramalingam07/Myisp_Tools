# 🚀 Quick Start Guide - PostgreSQL Integration

## ✅ What's Been Set Up

Your Azure DevOps Test Report Generator now has **full PostgreSQL integration** with a **live dashboard**!

### 📁 New Files Created:
- `database_setup.sql` - Database schema (tables, indexes)
- `database_utils.py` - Database connection utilities
- `api_server.py` - Flask REST API server
- `dynamic_report.html` - Live dashboard with auto-refresh
- `setup.bat` / `setup.sh` - Automated setup scripts
- `SETUP_GUIDE.md` - Complete documentation

### ⚡ What Changed in ProdSanity_Report.py:
- ✅ Added PostgreSQL support (automatic save after each run)
- ✅ Database integration is **optional** - works with or without PostgreSQL
- ✅ All existing functionality preserved

---

## 🏁 How to Use It (3 Steps)

### **Step 1: Setup Database** (One-time only)
```powershell
# Run the automated setup script:
.\setup.bat
```

**What it does:**
- Installs required packages (psycopg2, flask, flask-cors)
- Creates database tables
- Tests the connection

**Manual setup alternative:**
```powershell
# 1. Install packages
pip install psycopg2-binary flask flask-cors

# 2. Create database tables
psql -U postgres -d myisp_tools -f database_setup.sql
```

---

### **Step 2: Generate Report**
```powershell
# Run your report generator as usual:
python ProdSanity_Report.py
```

**What happens:**
- ✅ Connects to Azure DevOps (same as before)
- ✅ Generates HTML + Excel reports (same as before)
- ✅ **NEW:** Automatically saves data to PostgreSQL database

**Console output:**
```
💾 Saving data to PostgreSQL database...
   ✅ Data saved successfully to database
```

---

### **Step 3: View Live Dashboard**

#### **Option A: Run API Server + Open Dashboard**
```powershell
# 1. Start the API server:
python api_server.py

# 2. In your browser, open:
http://localhost:5000
```

#### **Option B: Open HTML File Directly**
```powershell
# Open in default browser:
start dynamic_report.html
```

The dashboard will:
- 📊 Show real-time statistics from PostgreSQL
- 🔄 Auto-refresh every 30 seconds
- 🔍 Interactive filtering by status/type
- 📈 Display latest report data

---

## 💡 Key Features

### **Static Reports** (Always Generated)
- 📄 `Prod_Execution_Report_[timestamp].html` - Offline report
- 📊 `Prod_Execution_Report_[timestamp].xlsx` - Excel format

### **Live Dashboard** (New!)
- 🌐 Real-time data from PostgreSQL
- 🔄 Auto-refresh (no manual reload needed)
- 🎨 Modern responsive UI
- 📱 Works on mobile/tablet

---

## 🔧 Troubleshooting

### Error: "Cannot connect to PostgreSQL"
**Solution:** Ensure PostgreSQL is running and database exists
```powershell
# Check if PostgreSQL is running:
Get-Service postgresql*

# Create database if missing:
psql -U postgres -c "CREATE DATABASE myisp_tools;"
```

---

### Error: "ModuleNotFoundError: No module named 'psycopg2'"
**Solution:** Install required packages
```powershell
pip install psycopg2-binary flask flask-cors
```

---

### Dashboard shows "No data available"
**Solution:** Generate at least one report first
```powershell
# Run the report generator:
python ProdSanity_Report.py
```

---

### API server won't start (port 5000 in use)
**Solution:** Change the port in `api_server.py`
```python
# Line at bottom of api_server.py:
app.run(debug=True, port=5001)  # Change to 5001
```

---

## 📊 Database Schema

### **Tables:**
- `test_executions` - All test case data (1 row per test)
- `report_metadata` - Report summary info (1 row per report run)

### **Query Examples:**
```sql
-- Get latest report statistics:
SELECT * FROM report_metadata ORDER BY created_at DESC LIMIT 1;

-- Get all failed tests from latest report:
SELECT test_case_name, outcome, bug_ids 
FROM test_executions 
WHERE report_id = (SELECT id FROM report_metadata ORDER BY created_at DESC LIMIT 1)
AND outcome = 'Failed';

-- Count tests by status:
SELECT outcome, COUNT(*) 
FROM test_executions 
WHERE report_id = (SELECT id FROM report_metadata ORDER BY created_at DESC LIMIT 1)
GROUP BY outcome;
```

---

## 🌐 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard UI |
| `GET /api/health` | Health check |
| `GET /api/statistics/latest` | Latest report stats |
| `GET /api/test-data/latest` | Latest test data |
| `GET /api/reports` | All report history |

**Example API call:**
```powershell
# Get latest statistics:
Invoke-RestMethod http://localhost:5000/api/statistics/latest
```

---

## 🎯 Workflow Summary

```
1. Run: python ProdSanity_Report.py
   ↓
2. Data saved to PostgreSQL automatically
   ↓
3. Static HTML + Excel reports generated
   ↓
4. Run: python api_server.py
   ↓
5. Open: http://localhost:5000
   ↓
6. View live dashboard with real-time data
```

---

## 📖 Full Documentation

For detailed setup, troubleshooting, and advanced features, see:
- **SETUP_GUIDE.md** - Complete setup documentation
- **database_setup.sql** - Database schema with comments
- **api_server.py** - API endpoint documentation

---

## ✨ Next Steps

1. Run `.\setup.bat` to complete database setup
2. Generate your first report: `python ProdSanity_Report.py`
3. Start API server: `python api_server.py`
4. Open dashboard: `http://localhost:5000`

**Enjoy your new live dashboard!** 🎉
