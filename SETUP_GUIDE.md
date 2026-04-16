# PostgreSQL Integration Setup Guide

## 📋 Prerequisites

1. **PostgreSQL** installed and running
2. **Python packages** installed
3. **Database created**

## 🚀 Quick Setup

### Step 1: Install Required Python Packages

```bash
pip install psycopg2-binary flask flask-cors
```

### Step 2: Create Database

Open PostgreSQL and run:

```sql
CREATE DATABASE myisp_tools;
```

### Step 3: Create Tables

Run the database setup script:

```bash
# Connect to PostgreSQL
psql -U postgres -d myisp_tools

# Run the SQL script
\i database_setup.sql
```

Or manually:

```bash
psql -U postgres -d myisp_tools -f database_setup.sql
```

### Step 4: Update Database Configuration (if needed)

If your PostgreSQL setup is different, update these files:
- `database_utils.py` (lines 10-16)
- `api_server.py` (lines 13-19)

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'myisp_tools',
    'user': 'postgres',
    'password': 'postgres123'  # Change this!
}
```

### Step 5: Generate Test Data

Run the report generator:

```bash
python ProdSanity_Report.py
```

Select option 1, 2, or 3. Data will be saved to PostgreSQL automatically.

### Step 6: Start API Server

```bash
python api_server.py
```

You should see:
```
🚀 Starting API Server...
📊 Database: myisp_tools @ localhost:5432
🌐 Server: http://localhost:5000
📡 API Endpoint: http://localhost:5000/api/test-data/latest
```

### Step 7: Open Dynamic Report

Open `dynamic_report.html` in your browser:
```bash
start dynamic_report.html
```

Or navigate to: http://localhost:5000

## 📊 Features

### Live Dashboard
- ✅ Real-time data from PostgreSQL
- 🔄 Auto-refresh every 30 seconds
- 🔍 Advanced filtering (Search, Status, Type)
- 📈 Interactive statistics cards

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/health` | Health check |
| `GET /api/statistics/latest` | Latest test statistics |
| `GET /api/test-data/latest` | Latest test execution data |
| `GET /api/reports` | List all reports |
| `GET /api/reports/<id>` | Get specific report |

### Example API Usage

```bash
# Get statistics
curl http://localhost:5000/api/statistics/latest

# Get test data
curl http://localhost:5000/api/test-data/latest

# Check health
curl http://localhost:5000/api/health
```

## 🔧 Troubleshooting

### Database Connection Error

**Error:** `Database connection failed`

**Solution:**
1. Verify PostgreSQL is running:
   ```bash
   # Windows
   pg_ctl status -D "C:\Program Files\PostgreSQL\15\data"
   
   # Linux/Mac
   sudo systemctl status postgresql
   ```

2. Check credentials in `database_utils.py` and `api_server.py`

3. Test connection:
   ```bash
   psql -U postgres -d myisp_tools
   ```

### No Data in Report

**Error:** Empty table in HTML

**Solution:**
1. Run `ProdSanity_Report.py` first to generate data
2. Verify data exists:
   ```sql
   SELECT COUNT(*) FROM test_executions;
   SELECT * FROM report_metadata ORDER BY generated_at DESC LIMIT 1;
   ```

### API Server Not Starting

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -i :5000
kill -9 <PID>
```

### CORS Error in Browser

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
- Flask-CORS is already configured in `api_server.py`
- Open developer console (F12) for more details
- Try accessing directly: http://localhost:5000/dynamic_report.html

## 📁 File Structure

```
Prod_Sanity_Report/
├── ProdSanity_Report.py          # Main report generator (updated)
├── database_setup.sql             # PostgreSQL schema
├── database_utils.py              # Database connection utilities
├── api_server.py                  # Flask API server
├── dynamic_report.html            # Live dashboard (NEW!)
├── Prod_Execution_Report.html     # Static HTML report
├── Prod_Execution_Report.xlsx     # Excel report
└── SETUP_GUIDE.md                 # This file
```

## 🎯 Workflow

1. **Generate Reports:** Run `ProdSanity_Report.py`
   - Fetches data from Azure DevOps
   - Saves to PostgreSQL
   - Generates static HTML + Excel

2. **Start API Server:** Run `api_server.py`
   - Serves data from PostgreSQL
   - Provides REST API endpoints

3. **View Live Dashboard:** Open `dynamic_report.html`
   - Connects to API
   - Displays real-time data
   - Auto-refreshes

## 🔒 Security Notes

**⚠️ Important:** Change default PostgreSQL password!

```sql
ALTER USER postgres WITH PASSWORD 'your_secure_password';
```

Then update:
- `database_utils.py`
- `api_server.py`

## 📞 Support

For issues:
1. Check PostgreSQL logs
2. Check API server console
3. Check browser console (F12)
4. Verify database has data

## ✅ Verification Checklist

- [ ] PostgreSQL installed and running
- [ ] Python packages installed (`psycopg2-binary`, `flask`, `flask-cors`)
- [ ] Database `myisp_tools` created
- [ ] Tables created (`test_executions`, `report_metadata`)
- [ ] `ProdSanity_Report.py` executed successfully
- [ ] `api_server.py` running on port 5000
- [ ] `dynamic_report.html` opens and displays data

## 🎉 Success!

If everything works, you should see:
- ✅ Green "LIVE" indicator
- 📊 Statistics cards populated
- 📋 Test execution table with data
- 🔄 Auto-refresh working
