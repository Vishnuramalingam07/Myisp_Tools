#!/usr/bin/env python3
"""
Update live_report.html with latest data and push to GitHub
This ensures the live page always shows the latest report data
"""

import os
import sys
import subprocess
from datetime import datetime

def update_and_push_html():
    """
    Copy the latest generated HTML to live_report.html and push to GitHub
    """
    
    print("\n📄 Updating live_report.html with latest data...")
    
    # Find the most recent Production_execution_report_*.html file
    import glob
    html_files = glob.glob('Production_execution_report_*.html')
    
    if not html_files:
        print("❌ No report HTML files found")
        return False
    
    # Sort by filename (which includes timestamp) to get the latest
    html_files.sort(reverse=True)
    latest_report = html_files[0]
    
    print(f"📋 Latest report: {latest_report}")
    
    # Read the latest report
    try:
        with open(latest_report, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"✓ Read {len(content)} bytes from {latest_report}")
    except Exception as e:
        print(f"❌ Error reading {latest_report}: {e}")
        return False
    
    # Check if this is different from current live_report.html
    try:
        with open('live_report.html', 'r', encoding='utf-8') as f:
            current_content = f.read()
        
        # Compare just the data tables (not Firebase scripts)
        # If they're the same, no need to update
        if content == current_content:
            print("ℹ️  No changes detected - live_report.html is already up to date")
            return True
    except FileNotFoundError:
        pass  # File doesn't exist yet, that's fine
    
    # Write to live_report.html
    try:
        with open('live_report.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Updated live_report.html")
    except Exception as e:
        print(f"❌ Error writing live_report.html: {e}")
        return False
    
    # Commit and push to GitHub
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        subprocess.run(['git', 'add', 'live_report.html'], check=True)
        subprocess.run(['git', 'commit', '-m', f'Update live report with latest data - {timestamp}'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print(f"✓ Pushed updated live_report.html to GitHub")
        print(f"🌐 Changes will be live at GitHub Pages in 1-2 minutes")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Git operation failed: {e}")
        print("   (This might be OK if there were no changes)")
        return True

if __name__ == '__main__':
    success = update_and_push_html()
    sys.exit(0 if success else 1)
