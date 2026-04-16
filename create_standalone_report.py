"""
Generate a self-contained HTML report with embedded JSON data
This allows the report to work when opened locally (file:// protocol)
"""

import json
import sys

def create_standalone_report(json_file='latest_report.json', output_file='standalone_report.html'):
    """Create HTML report with embedded JSON data"""
    
    # Read JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: {json_file} not found!")
        print(f"   Run 'python ProdSanity_Report.py' first to generate it.")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {json_file}: {e}")
        return False
    
    # Read HTML template
    try:
        with open('live_report.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: live_report.html not found!")
        return False
    
    # Convert data to JavaScript
    json_data_js = json.dumps(data, ensure_ascii=False, indent=2)
    
    # Replace the fetch logic with embedded data
    search_pattern = '''        // Configuration - Use relative path since both files are on GitHub Pages
        const JSON_FILE = './latest_report.json';
        
        let refreshInterval = 30; // seconds
        let countdownTimer = null;
        let refreshTimer = null;
        let currentData = null;

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {
            refreshData();
            startAutoRefresh();
        });

        // Fetch data from JSON file
        async function refreshData() {
            console.log('🔄 refreshData() called');
            try {
                // Add cache-busting parameter to force fresh data
                const url = `${JSON_FILE}?t=${Date.now()}`;
                console.log('📡 Fetching:', url);
                
                const response = await fetch(url, {
                    cache: 'no-cache',
                    headers: {
                        'Cache-Control': 'no-cache'
                    }
                });

                console.log('📥 Response status:', response.status);
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                console.log('✅ Data loaded:', data.statistics.total_tests, 'tests');
                currentData = data;'''
    
    replacement = f'''        // ⚡ EMBEDDED DATA MODE - Works with file:// protocol
        // Data generated: {data.get('timestamp_display', 'N/A')}
        const EMBEDDED_DATA = {json_data_js};
        
        let refreshInterval = 0; // Disabled for embedded mode
        let countdownTimer = null;
        let refreshTimer = null;
        let currentData = EMBEDDED_DATA;

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', () => {{
            loadEmbeddedData();
        }});

        // Load embedded data (no fetch needed)
        function loadEmbeddedData() {{
            console.log('✅ Loading embedded data...');
            try {{
                const data = EMBEDDED_DATA;
                console.log('✅ Data loaded:', data.statistics.total_tests, 'tests');
                currentData = data;'''
    
    # Replace in HTML
    if search_pattern in html_content:
        html_content = html_content.replace(search_pattern, replacement)
        
        # Also update the title to indicate standalone mode
        html_content = html_content.replace(
            '<title>Live Production Execution Report</title>',
            '<title>Production Execution Report (Standalone)</title>'
        )
        
        # Update the live indicator text
        html_content = html_content.replace(
            '<span id="liveIndicator" class="live-indicator">',
            '<span id="liveIndicator" class="static-indicator">'
        )
        html_content = html_content.replace(
            '<span class="live-dot"></span>LIVE',
            'EMBEDDED DATA'
        )
        
        # Disable refresh controls
        html_content = html_content.replace(
            '<div class="countdown" id="countdown">Next update in 30s</div>',
            '<div class="countdown">Standalone mode - data embedded</div>'
        )
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Created: {output_file}")
        print(f"   📊 Total tests: {data['statistics']['total_tests']}")
        print(f"   📅 Generated: {data.get('timestamp_display', 'N/A')}")
        print(f"\n💡 You can now open this file directly:")
        print(f"   file:///{output_file}")
        return True
    else:
        print(f"❌ Error: Could not find expected code pattern in live_report.html")
        print(f"   The file may have been modified.")
        return False

if __name__ == '__main__':
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    success = create_standalone_report()
    sys.exit(0 if success else 1)
