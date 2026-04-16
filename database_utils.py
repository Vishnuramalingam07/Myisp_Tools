"""
Database utilities for storing test execution data in PostgreSQL
"""

import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'myisp_tools',
    'user': 'postgres',
    'password': 'postgres123'
}

def get_db_connection():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"      ⚠️  Database connection error: {e}")
        return None

def save_test_data_to_db(test_data, report_type='Prod Execution'):
    """Save test execution data to PostgreSQL"""
    if not test_data:
        print(f"      ⚠️  No test data to save")
        return False
    
    conn = get_db_connection()
    if not conn:
        print(f"      ⚠️  Could not connect to database")
        return False
    
    try:
        cursor = conn.cursor()
        
        # Calculate statistics
        total = len(test_data)
        passed = sum(1 for t in test_data if t.get('outcome') == 'Passed')
        failed = sum(1 for t in test_data if t.get('outcome') == 'Failed')
        blocked = sum(1 for t in test_data if t.get('outcome') == 'Blocked')
        not_run = sum(1 for t in test_data if t.get('outcome') == 'Not Run')
        automation = sum(1 for t in test_data if t.get('test_type') == 'Automation')
        manual = sum(1 for t in test_data if t.get('test_type') == 'Manual')
        total_bugs = sum(t.get('bug_count', 0) for t in test_data)
        
        # Insert report metadata
        cursor.execute("""
            INSERT INTO report_metadata 
            (report_name, report_type, total_tests, passed, failed, blocked, 
             not_run, automation_count, manual_count, total_bugs)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (
            f"{report_type} - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            report_type,
            total, passed, failed, blocked, not_run, automation, manual, total_bugs
        ))
        
        report_id = cursor.fetchone()[0]
        
        # Prepare test data for batch insert
        test_records = []
        for test in test_data:
            test_records.append((
                test.get('test_case_id'),
                test.get('test_case_title', 'Unknown'),
                test.get('priority', 'N/A'),
                test.get('test_type', 'Manual'),
                test.get('outcome', 'Not Run'),
                test.get('assigned_to', 'Unassigned'),
                test.get('lead', 'Unassigned'),
                test.get('module', 'Unknown'),
                test.get('requirement_id', 'N/A'),
                test.get('requirement_title', 'No Linked US'),
                test.get('bug_count', 0),
                test.get('bug_details', 'No Bugs'),
                test.get('suite_name', 'Unknown'),
                report_type
            ))
        
        # Batch insert test execution data
        execute_batch(cursor, """
            INSERT INTO test_executions 
            (test_case_id, test_case_title, priority, test_type, outcome,
             assigned_to, lead, module, requirement_id, requirement_title,
             bug_count, bug_details, suite_name, report_type)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, test_records)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"      ✅ Saved {len(test_records)} test records to database (Report ID: {report_id})")
        return True
        
    except Exception as e:
        print(f"      ❌ Database save error: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def test_database_connection():
    """Test database connection and setup"""
    print(f"\n🔌 Testing Database Connection...")
    print(f"   Host: {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"   Database: {DB_CONFIG['database']}")
    
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            print(f"   ✅ Connected to PostgreSQL: {version[0].split(',')[0]}")
            
            # Check if tables exist
            cursor.execute("""
                SELECT table_name FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('test_executions', 'report_metadata')
            """)
            tables = cursor.fetchall()
            
            if len(tables) == 2:
                print(f"   ✅ Database tables found: test_executions, report_metadata")
            else:
                print(f"   ⚠️  Database tables not found. Run database_setup.sql first!")
            
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print(f"   ❌ Database test failed: {e}")
            conn.close()
            return False
    else:
        print(f"   ❌ Could not connect to database")
        return False
