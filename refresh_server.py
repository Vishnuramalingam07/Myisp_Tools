"""
Simple Flask API Server to Trigger Report Refresh
Run with: python refresh_server.py
Then use the "Refresh Data" button in live_report.html
"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import subprocess
import threading
import os
import sys
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for local development

# Global status tracker
refresh_status = {
    'running': False,
    'last_run': None,
    'last_status': 'idle',
    'last_error': None,
    'output': []
}

def run_refresh():
    """Run the ProdSanity_Report.py script in background"""
    global refresh_status
    
    refresh_status['running'] = True
    refresh_status['last_status'] = 'running'
    refresh_status['output'] = []
    refresh_status['last_error'] = None
    
    try:
        print(f"\n{'='*80}")
        print(f"🔄 Starting report refresh at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}\n")
        
        # Run the Python script and capture output
        process = subprocess.Popen(
            [sys.executable, 'ProdSanity_Report.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace problematic characters instead of crashing
            bufsize=1
        )
        
        # Capture output in real-time
        for line in process.stdout:
            line = line.strip()
            if line:
                print(line)
                refresh_status['output'].append(line)
        
        # Wait for completion
        return_code = process.wait()
        
        if return_code == 0:
            refresh_status['last_status'] = 'success'
            refresh_status['last_run'] = datetime.now().isoformat()
            print(f"\n✅ Report refresh completed successfully!")
        else:
            error_output = process.stderr.read()
            refresh_status['last_status'] = 'error'
            refresh_status['last_error'] = error_output or f"Process exited with code {return_code}"
            print(f"\n❌ Report refresh failed with code {return_code}")
            if error_output:
                print(f"Error: {error_output}")
    
    except Exception as e:
        refresh_status['last_status'] = 'error'
        refresh_status['last_error'] = str(e)
        print(f"\n❌ Exception during refresh: {e}")
    
    finally:
        refresh_status['running'] = False
        print(f"\n{'='*80}\n")

@app.route('/api/refresh', methods=['POST'])
def trigger_refresh():
    """Endpoint to trigger report refresh"""
    global refresh_status
    
    if refresh_status['running']:
        return jsonify({
            'status': 'already_running',
            'message': 'Report refresh is already in progress'
        }), 409
    
    # Start refresh in background thread
    thread = threading.Thread(target=run_refresh, daemon=True)
    thread.start()
    
    return jsonify({
        'status': 'started',
        'message': 'Report refresh started in background'
    }), 202

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current refresh status"""
    return jsonify(refresh_status)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Report Refresh API',
        'timestamp': datetime.now().isoformat()
    })

# Serve the live_report.html file
@app.route('/')
def serve_report():
    """Serve the live report HTML"""
    return send_from_directory('.', 'live_report.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve other static files"""
    return send_from_directory('.', path)

if __name__ == '__main__':
    print(f"\n{'='*80}")
    print("🚀 REPORT REFRESH API SERVER")
    print(f"{'='*80}")
    print("\n📡 Server Configuration:")
    print("   • API Server: http://localhost:5000")
    print("   • Live Report: http://localhost:5000/")
    print("   • Health Check: http://localhost:5000/api/health")
    print("   • Refresh Endpoint: http://localhost:5000/api/refresh")
    print("   • Status Endpoint: http://localhost:5000/api/status")
    print("\n💡 Usage:")
    print("   1. Open: http://localhost:5000/ in your browser")
    print("   2. Click the '🔄 Refresh from Azure DevOps' button")
    print("   3. Wait for the script to complete")
    print("   4. Page will auto-reload with fresh data")
    print(f"\n{'='*80}\n")
    
    # Check if requirements are installed
    try:
        import flask_cors
    except ImportError:
        print("⚠️  WARNING: flask-cors not installed")
        print("   Install with: pip install flask-cors")
        print()
    
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
