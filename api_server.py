"""
Flask API Server for Test Execution Reports
Serves data from PostgreSQL database to HTML frontend
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Shared data storage file
SHARED_DATA_FILE = 'shared_report_data.json'

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
        print(f"Database connection error: {e}")
        return None

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'dynamic_report.html')

@app.route('/api/reports', methods=['GET'])
def get_reports():
    """Get list of all available reports"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT id, report_name, report_type, total_tests, passed, failed, 
                   blocked, not_run, automation_count, manual_count, total_bugs,
                   generated_at
            FROM report_metadata
            ORDER BY generated_at DESC
            LIMIT 50
        """)
        reports = cursor.fetchall()
        
        # Convert datetime objects to strings
        for report in reports:
            if report['generated_at']:
                report['generated_at'] = report['generated_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(reports)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reports/<int:report_id>', methods=['GET'])
def get_report_details(report_id):
    """Get detailed test data for a specific report"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get report metadata
        cursor.execute("""
            SELECT * FROM report_metadata WHERE id = %s
        """, (report_id,))
        metadata = cursor.fetchone()
        
        if not metadata:
            return jsonify({'error': 'Report not found'}), 404
        
        # Convert datetime to string
        if metadata['generated_at']:
            metadata['generated_at'] = metadata['generated_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(metadata)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/test-data/latest', methods=['GET'])
def get_latest_test_data():
    """Get latest test execution data"""
    report_type = request.args.get('report_type', '')
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get the latest report metadata
        if report_type:
            cursor.execute("""
                SELECT id FROM report_metadata 
                WHERE report_type = %s
                ORDER BY generated_at DESC 
                LIMIT 1
            """, (report_type,))
        else:
            cursor.execute("""
                SELECT id FROM report_metadata 
                ORDER BY generated_at DESC 
                LIMIT 1
            """)
        
        latest_report = cursor.fetchone()
        
        if not latest_report:
            return jsonify({'error': 'No reports found'}), 404
        
        # Get test data from the time period
        cursor.execute("""
            SELECT test_case_id, test_case_title, priority, test_type, outcome,
                   assigned_to, lead, module, requirement_id, requirement_title,
                   bug_count, bug_details, suite_name, created_at
            FROM test_executions
            WHERE created_at >= (
                SELECT generated_at FROM report_metadata WHERE id = %s
            )
            ORDER BY created_at DESC
        """, (latest_report['id'],))
        
        test_data = cursor.fetchall()
        
        # Convert datetime objects to strings
        for test in test_data:
            if test['created_at']:
                test['created_at'] = test['created_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(test_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistics/latest', methods=['GET'])
def get_latest_statistics():
    """Get statistics for the latest report"""
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT total_tests, passed, failed, blocked, not_run,
                   automation_count, manual_count, total_bugs, generated_at
            FROM report_metadata
            ORDER BY generated_at DESC
            LIMIT 1
        """)
        
        stats = cursor.fetchone()
        
        if not stats:
            return jsonify({'error': 'No statistics found'}), 404
        
        # Convert datetime to string
        if stats['generated_at']:
            stats['generated_at'] = stats['generated_at'].isoformat()
        
        cursor.close()
        conn.close()
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint - for collaborative features, DB is optional"""
    conn = get_db_connection()
    db_status = 'connected' if conn else 'disconnected'
    if conn:
        conn.close()
    
    # Collaborative sync works without database (uses JSON file)
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'collaborative_sync': 'active'
    })

@app.route('/api/shared-data/<tab_id>', methods=['GET'])
def get_shared_data(tab_id):
    """Get shared data for a specific tab"""
    try:
        if os.path.exists(SHARED_DATA_FILE):
            with open(SHARED_DATA_FILE, 'r') as f:
                all_data = json.load(f)
                tab_data = all_data.get(tab_id, {})
                return jsonify({
                    'success': True,
                    'data': tab_data,
                    'timestamp': all_data.get(f'{tab_id}_timestamp', None)
                })
        return jsonify({'success': True, 'data': {}, 'timestamp': None})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/shared-data/<tab_id>', methods=['POST'])
def save_shared_data(tab_id):
    """Save shared data for a specific tab"""
    try:
        data = request.get_json()
        
        # Load existing data
        all_data = {}
        if os.path.exists(SHARED_DATA_FILE):
            with open(SHARED_DATA_FILE, 'r') as f:
                all_data = json.load(f)
        
        # Update tab data
        all_data[tab_id] = data.get('data', {})
        all_data[f'{tab_id}_timestamp'] = datetime.now().isoformat()
        all_data[f'{tab_id}_user'] = data.get('user', 'Anonymous')
        
        # Save back to file
        with open(SHARED_DATA_FILE, 'w') as f:
            json.dump(all_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': 'Data saved successfully',
            'timestamp': all_data[f'{tab_id}_timestamp']
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/shared-data', methods=['GET'])
def get_all_shared_data():
    """Get all shared data for all tabs"""
    try:
        if os.path.exists(SHARED_DATA_FILE):
            with open(SHARED_DATA_FILE, 'r') as f:
                all_data = json.load(f)
                return jsonify({'success': True, 'data': all_data})
        return jsonify({'success': True, 'data': {}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting API Server...")
    print(f"📊 Database: {DB_CONFIG['database']} @ {DB_CONFIG['host']}:{DB_CONFIG['port']}")
    print(f"🌐 Server: http://localhost:5000")
    print(f"📡 API Endpoint: http://localhost:5000/api/test-data/latest")
    app.run(debug=True, host='0.0.0.0', port=5000)
