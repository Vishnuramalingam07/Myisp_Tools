#!/usr/bin/env python3
"""
Upload latest_report.json to Firebase Realtime Database
Used by GitHub Actions to sync report data automatically
"""

import json
import os
import sys
import requests
from datetime import datetime

# Firebase configuration from environment or defaults
FIREBASE_DATABASE_URL = os.getenv('FIREBASE_DATABASE_URL', 'https://myisptools-default-rtdb.firebaseio.com')
FIREBASE_PATH = os.getenv('FIREBASE_PATH', 'prodSanityReport')
REPORT_FILE = os.getenv('REPORT_FILE', 'latest_report.json')

def sanitize_firebase_key(key):
    """
    Sanitize key names for Firebase Realtime Database.
    Firebase keys cannot contain: . $ # [ ] /
    
    Args:
        key: Original key name
        
    Returns:
        Sanitized key safe for Firebase
    """
    if not isinstance(key, str):
        return str(key)
    
    # Replace invalid characters
    sanitized = key.replace('.', '_')
    sanitized = sanitized.replace('$', '_')
    sanitized = sanitized.replace('#', '_')
    sanitized = sanitized.replace('[', '(')
    sanitized = sanitized.replace(']', ')')
    sanitized = sanitized.replace('/', '-')
    
    # Remove leading/trailing whitespace
    sanitized = sanitized.strip()
    
    # Ensure key is not empty
    if not sanitized:
        sanitized = 'empty_key'
    
    return sanitized

def sanitize_firebase_data(data):
    """
    Recursively sanitize all keys in nested dictionaries/lists.
    
    Args:
        data: Dictionary, list, or primitive value
        
    Returns:
        Sanitized data structure
    """
    if isinstance(data, dict):
        # Sanitize all keys in dictionary
        return {
            sanitize_firebase_key(k): sanitize_firebase_data(v)
            for k, v in data.items()
        }
    elif isinstance(data, list):
        # Recursively sanitize list items
        return [sanitize_firebase_data(item) for item in data]
    else:
        # Return primitive values as-is
        return data

def upload_to_firebase(json_file, database_url, firebase_path):
    """
    Upload JSON data to Firebase Realtime Database using REST API
    
    Args:
        json_file: Path to the JSON file to upload
        database_url: Firebase database URL (e.g., https://myproject-default-rtdb.firebaseio.com)
        firebase_path: Path in the database (e.g., prodSanityReport)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    print(f"\n🔥 Uploading to Firebase Realtime Database...")
    print(f"   File: {json_file}")
    print(f"   Database: {database_url}")
    print(f"   Path: {firebase_path}")
    
    # Check if file exists
    if not os.path.exists(json_file):
        print(f"❌ Error: File not found: {json_file}")
        return False
    
    # Read JSON data
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✓ Loaded {len(json.dumps(data))} bytes from {json_file}")
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return False
    
    # Sanitize data for Firebase (remove invalid characters from keys)
    print(f"🔧 Sanitizing data for Firebase...")
    data = sanitize_firebase_data(data)
    print(f"✓ Data sanitized (Firebase-safe keys)")
    
    # Add upload metadata
    data['uploaded_at'] = datetime.now().isoformat()
    data['upload_source'] = 'github_actions'
    
    # Construct Firebase REST API URL
    # Format: https://DATABASE_URL/PATH.json
    firebase_url = f"{database_url.rstrip('/')}/{firebase_path}.json"
    
    try:
        # Upload data using PUT request (replaces entire node)
        print(f"   Uploading to: {firebase_url}")
        response = requests.put(
            firebase_url,
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ Successfully uploaded to Firebase!")
            print(f"   Status: {response.status_code}")
            print(f"   Response size: {len(response.text)} bytes")
            
            # Verify data was written
            verify_response = requests.get(firebase_url, timeout=10)
            if verify_response.status_code == 200:
                verify_data = verify_response.json()
                if verify_data and 'generated_at' in verify_data:
                    print(f"✓ Verified: Data timestamp = {verify_data['generated_at']}")
                else:
                    print(f"⚠️  Warning: Data verification incomplete")
            
            return True
        else:
            print(f"❌ Firebase upload failed!")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error uploading to Firebase: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


def main():
    """Main entry point"""
    print("=" * 60)
    print("Firebase Upload Script")
    print("=" * 60)
    
    # Show configuration
    print(f"\n📋 Configuration:")
    print(f"   Database URL: {FIREBASE_DATABASE_URL}")
    print(f"   Firebase Path: {FIREBASE_PATH}")
    print(f"   Report File: {REPORT_FILE}")
    
    # Upload to Firebase
    success = upload_to_firebase(REPORT_FILE, FIREBASE_DATABASE_URL, FIREBASE_PATH)
    
    if success:
        print(f"\n✅ Upload complete!")
        print(f"\n🌐 View live report at:")
        print(f"   https://vishnuramalingam07.github.io/Myisp_Tools/live_report.html")
        sys.exit(0)
    else:
        print(f"\n❌ Upload failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
