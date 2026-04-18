#!/usr/bin/env python3
"""
Add Firebase integration to generated report HTML
This preserves the Firebase dynamic loading while keeping report data fresh
"""

import sys
import re

def add_firebase_to_html(input_html, output_html):
    """
    Add Firebase SDK and integration code to the generated HTML report
    """
    
    print(f"\n🔥 Adding Firebase integration to {input_html}...")
    
    try:
        with open(input_html, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"❌ Error reading {input_html}: {e}")
        return False
    
    # Firebase SDK and initialization code to inject
    firebase_code = '''    <script src="https://cdn.jsdelivr.net/npm/exceljs@4.3.0/dist/exceljs.min.js"></script>
    <!-- Firebase SDK v9 (Modular) -->
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app-compat.js"></script>
    <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-database-compat.js"></script>
    <!-- Firebase Configuration -->
    <script>
        // Firebase configuration
        const firebaseConfig = {
            apiKey: "AIzaSyB_9XEWyPOsM4p8aCdgHo4zOljH-eGPLdM",
            authDomain: "myisptools.firebaseapp.com",
            databaseURL: "https://myisptools-default-rtdb.firebaseio.com",
            projectId: "myisptools",
            storageBucket: "myisptools.firebasestorage.app",
            messagingSenderId: "231946416648",
            appId: "1:231946416648:web:8123b8e35ab43c0b2997bd"
        };
        
        // Initialize Firebase
        firebase.initializeApp(firebaseConfig);
        const database = firebase.database();
        console.log('✓ Firebase initialized');
    </script>'''
    
    # Find the exceljs script tag and replace it with Firebase code
    pattern = r'<script src="https://cdn\.jsdelivr\.net/npm/exceljs@[^"]+"></script>'
    
    if re.search(pattern, content):
        content = re.sub(pattern, firebase_code, content)
        print("✓ Replaced exceljs script with Firebase integration")
    else:
        # If pattern not found, try to inject before </head>
        if '</head>' in content:
            content = content.replace('</head>', firebase_code + '\n    </head>')
            print("✓ Injected Firebase code before </head>")
        else:
            print("⚠️  Could not find injection point for Firebase code")
            return False
    
    # Write the updated HTML
    try:
        with open(output_html, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Wrote Firebase-integrated HTML to {output_html}")
        return True
    except Exception as e:
        print(f"❌ Error writing {output_html}: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python add_firebase_integration.py <input_html> <output_html>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    success = add_firebase_to_html(input_file, output_file)
    sys.exit(0 if success else 1)
