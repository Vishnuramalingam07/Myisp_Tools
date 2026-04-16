#!/bin/bash

echo "========================================"
echo "PostgreSQL Integration Setup"
echo "========================================"
echo ""

echo "Step 1: Installing Python packages..."
pip install psycopg2-binary flask flask-cors
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install packages"
    exit 1
fi
echo "✓ Packages installed successfully"
echo ""

echo "Step 2: Checking PostgreSQL connection..."
python3 -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5432, database='myisp_tools', user='postgres', password='postgres123'); print('✓ Database connection successful'); conn.close()"
if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Cannot connect to PostgreSQL"
    echo "Please ensure:"
    echo "  1. PostgreSQL is running"
    echo "  2. Database 'myisp_tools' exists"
    echo "  3. Username/password are correct"
    echo ""
    echo "To create database, run in psql:"
    echo "  CREATE DATABASE myisp_tools;"
    echo ""
    exit 1
fi
echo ""

echo "Step 3: Creating database tables..."
psql -U postgres -d myisp_tools -f database_setup.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create tables"
    echo "Please run manually: psql -U postgres -d myisp_tools -f database_setup.sql"
    exit 1
fi
echo "✓ Tables created successfully"
echo ""

echo "Step 4: Testing database utilities..."
python3 -c "from database_utils import test_database_connection; test_database_connection()"
if [ $? -ne 0 ]; then
    echo "ERROR: Database utilities test failed"
    exit 1
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Run: python3 ProdSanity_Report.py"
echo "     (This will generate reports and save to database)"
echo ""
echo "  2. Run: python3 api_server.py"
echo "     (This will start the API server on port 5000)"
echo ""
echo "  3. Open: dynamic_report.html in your browser"
echo "     (This will show the live dashboard)"
echo ""
echo "========================================"
