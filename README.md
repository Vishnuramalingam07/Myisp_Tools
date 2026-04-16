# Azure DevOps Test Execution Report Generator 🚀

Professional test reporting tool that generates comprehensive HTML and Excel reports from Azure DevOps Test Plans, with optional PostgreSQL integration and live dashboard.

---

## 📋 Features

### Core Functionality
- ✅ **Azure DevOps Integration** - Connect to Test Plans, Suites, and Work Items
- ✅ **Multi-Format Reports** - Generate both HTML and Excel reports
- ✅ **Bug Tracking** - Automatic bug linking and severity tracking
- ✅ **Test Coverage** - Track manual vs automation coverage
- ✅ **Requirement Mapping** - Link test cases to user stories

### Enhanced Features
- 🗄️ **PostgreSQL Integration** (Optional) - Persistent data storage
- 🌐 **Live Dashboard** - Real-time updates with auto-refresh
- 📊 **REST API** - Access test data via JSON endpoints
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Color-coded status indicators

---

## 🏗️ Architecture

```
Azure DevOps Test Plans
         ↓
ProdSanity_Report.py (Main Script)
         ↓
    ┌────┴────┐
    ↓         ↓
Static      PostgreSQL
Reports     Database
(HTML/Excel)    ↓
            API Server
                ↓
           Live Dashboard
```

---

## 📁 Project Structure

```
Prod_Sanity_Report/
│
├── ProdSanity_Report.py       # Main report generator
├── database_setup.sql         # PostgreSQL schema
├── database_utils.py          # Database utilities
├── api_server.py              # Flask REST API
├── dynamic_report.html        # Live dashboard UI
│
├── setup.bat / setup.sh       # Automated setup scripts
├── QUICK_START.md             # Quick start guide
├── SETUP_GUIDE.md             # Detailed setup docs
└── README.md                  # This file
```

---

## ⚡ Quick Start

### Without PostgreSQL (Basic Usage)
```powershell
# 1. Install dependencies
pip install requests openpyxl

# 2. Configure Azure DevOps credentials in script
# Edit ProdSanity_Report.py lines 15-25

# 3. Run the generator
python ProdSanity_Report.py

# Output: HTML + Excel reports generated
```

### With PostgreSQL (Full Features)
```powershell
# 1. Run automated setup
.\setup.bat

# 2. Generate reports (saves to database automatically)
python ProdSanity_Report.py

# 3. Start API server
python api_server.py

# 4. Open live dashboard
start http://localhost:5000
```

**📖 Detailed Instructions:** See [QUICK_START.md](QUICK_START.md)

---

## 🔧 Configuration

### Azure DevOps Settings
Edit `ProdSanity_Report.py` (lines 15-30):

```python
ADO_CONFIG = {
    'org': 'your-organization',
    'project': 'your-project',
    'pat': 'your-personal-access-token',
    'plan_id': 1234567,
    'suite_id': 7654321,
    'target_suite_name': 'Your Suite Name',
}
```

### Database Settings (Optional)
Edit `database_utils.py`:

```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'myisp_tools',
    'user': 'postgres',
    'password': 'postgres123'
}
```

---

## 📊 Report Types

### 1. Static HTML Report
- **File:** `Prod_Execution_Report_[timestamp].html`
- **Features:**
  - Color-coded test status
  - Bug details and severity
  - Requirement traceability
  - Offline viewing
  - Responsive design

### 2. Excel Report
- **File:** `Prod_Execution_Report_[timestamp].xlsx`
- **Features:**
  - Structured data tables
  - Pivot-ready format
  - Color-coded cells
  - Multiple sheets

### 3. Live Dashboard (with PostgreSQL)
- **URL:** `http://localhost:5000`
- **Features:**
  - Real-time statistics
  - Auto-refresh (30s)
  - Interactive filtering
  - Historical data
  - API access

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Dashboard UI |
| `/api/health` | GET | Server health check |
| `/api/statistics/latest` | GET | Latest report summary |
| `/api/test-data/latest` | GET | Latest test execution data |
| `/api/reports` | GET | All report history |

**Example:**
```powershell
# Get latest statistics
curl http://localhost:5000/api/statistics/latest

# Response:
{
  "report_name": "Prod Execution Report",
  "total_tests": 1074,
  "manual_tests": 850,
  "automation_tests": 224,
  "passed": 950,
  "failed": 100,
  "not_executed": 24
}
```

---

## 🗄️ Database Schema

### test_executions
Stores individual test case execution data.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| report_id | INT | Foreign key to report_metadata |
| test_case_id | INT | Azure DevOps test case ID |
| test_case_name | TEXT | Test case title |
| outcome | VARCHAR(50) | Passed/Failed/Not Executed |
| test_type | VARCHAR(50) | Manual/Automation |
| priority | VARCHAR(20) | Test priority level |
| requirement_names | TEXT | Linked requirements |
| bug_ids | TEXT | Linked bug IDs |
| bug_count | INT | Number of bugs |
| created_at | TIMESTAMP | Record creation time |

### report_metadata
Stores report-level summary information.

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| report_name | VARCHAR(255) | Report title |
| suite_name | VARCHAR(255) | Test suite name |
| total_tests | INT | Total test count |
| manual_tests | INT | Manual test count |
| automation_tests | INT | Automation test count |
| passed | INT | Passed tests |
| failed | INT | Failed tests |
| not_executed | INT | Not executed tests |
| created_at | TIMESTAMP | Report generation time |

---

## 🛠️ Dependencies

### Required (Basic Usage)
- **Python 3.7+**
- **requests** - Azure DevOps API calls
- **openpyxl** - Excel report generation

### Optional (Full Features)
- **psycopg2-binary** - PostgreSQL connectivity
- **flask** - REST API server
- **flask-cors** - Cross-origin requests
- **PostgreSQL 12+** - Database server

**Install all:**
```powershell
pip install requests openpyxl psycopg2-binary flask flask-cors
```

---

## 📖 Documentation

- **[QUICK_START.md](QUICK_START.md)** - Fast setup guide
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Comprehensive documentation
- **[database_setup.sql](database_setup.sql)** - Database schema with comments

---

## 🐛 Troubleshooting

### Common Issues

**1. Azure DevOps Connection Failed**
- Verify PAT token has proper permissions (Test Management, Work Items Read)
- Check organization, project, and plan IDs
- Ensure PAT token hasn't expired

**2. PostgreSQL Connection Failed**
- Start PostgreSQL service: `Get-Service postgresql*`
- Create database: `psql -U postgres -c "CREATE DATABASE myisp_tools;"`
- Verify credentials in `database_utils.py`

**3. No Data in Dashboard**
- Run `python ProdSanity_Report.py` at least once
- Start API server: `python api_server.py`
- Check database has data: `SELECT COUNT(*) FROM test_executions;`

**4. Port 5000 Already in Use**
- Change port in `api_server.py`: `app.run(port=5001)`
- Update dashboard URL accordingly

---

## 🔐 Security Notes

### Azure DevOps PAT Token
- **Never commit PAT tokens to version control**
- Use environment variables: `os.getenv('ADO_PAT')`
- Set expiration dates on tokens

### Database Credentials
- Use strong passwords for production
- Restrict network access to database
- Consider using `.env` files for config

**Example .env usage:**
```python
from dotenv import load_dotenv
load_dotenv()

DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'password': os.getenv('DB_PASSWORD'),
}
```

---

## 📈 Performance Tips

### Large Test Suites (1000+ tests)
- **Parallel Processing:** Script uses ThreadPoolExecutor (10 workers)
- **Batch API Calls:** Reduces API calls via batching
- **Database Indexes:** Automatically created for fast queries

### Dashboard Performance
- **Pagination:** Consider adding for 10,000+ test cases
- **Caching:** API responses cached for 30 seconds
- **Database Tuning:** Add indexes on frequently queried columns

---

## 🚀 Deployment

### Local Development
```powershell
# Run everything locally
python ProdSanity_Report.py
python api_server.py
```

### GitHub Pages Deployment (Static Demo)

**Quick Deploy:**
```powershell
git add .
git commit -m "Deploy to GitHub Pages"
git push origin main
```

Your site will be live at: `https://YOUR_USERNAME.github.io/MyISP_Tools/Prod_Sanity_Report/`

**📖 Full Instructions:** See [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)

### Production Deployment (Full Stack)

**Frontend: GitHub Pages** (Static files)
- Automated deployment via GitHub Actions
- See [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)

**Backend Options:**

**Option 1: Azure App Service** ⭐ Recommended
```powershell
az webapp up --name myisp-api --runtime PYTHON:3.9
```

**Option 2: Docker Container**
```dockerfile
FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "api_server.py"]
```

**Option 3: Heroku**
```powershell
heroku create myisp-api
git push heroku main
```

---

## 📝 License

This project is internal tooling. Modify as needed for your organization.

---

## 👥 Support

For questions or issues:
1. Check **QUICK_START.md** for common setup issues
2. Review **SETUP_GUIDE.md** for detailed documentation
3. Contact your Azure DevOps administrator

---

## 🔄 Version History

### v3.0.0 (Current)
- ✅ Added PostgreSQL integration
- ✅ Live dashboard with REST API
- ✅ Auto-refresh functionality
- ✅ Database persistence layer

### v2.0.0
- ✅ HTML report generation
- ✅ Excel export functionality
- ✅ Enhanced bug tracking

### v1.0.0
- ✅ Initial release
- ✅ Azure DevOps connectivity
- ✅ Basic report generation

---

**Made with ❤️ for better test reporting**
