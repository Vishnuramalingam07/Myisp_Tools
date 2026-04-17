"""
Test script for collaborative live report functionality
Tests the API endpoints and verifies data sync works correctly
"""

import requests
import json
import time

# Configuration
API_BASE_URL = "http://localhost:5000/api"
TEST_TAB_ID = "prodSanityTab"

def print_status(message, status="INFO"):
    colors = {
        "INFO": "\033[94m",
        "SUCCESS": "\033[92m",
        "ERROR": "\033[91m",
        "WARNING": "\033[93m",
        "RESET": "\033[0m"
    }
    print(f"{colors.get(status, '')}{status}: {message}{colors['RESET']}")

def test_health_check():
    """Test if the API server is running"""
    print_status("Testing server health check...", "INFO")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print_status(f"Server is healthy: {data}", "SUCCESS")
            return True
        else:
            print_status(f"Server returned status {response.status_code}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Failed to connect to server: {e}", "ERROR")
        print_status("Make sure to start the server with: python api_server.py", "WARNING")
        return False

def test_save_data():
    """Test saving data to the server"""
    print_status("Testing data save...", "INFO")
    
    test_data = {
        "data": {
            "0": "Test User",
            "1": "Working fine",
            "2": "Test comment",
            "3": "In Progress"
        },
        "user": "Test User"
    }
    
    try:
        response = requests.post(
            f"{API_BASE_URL}/shared-data/{TEST_TAB_ID}",
            json=test_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print_status(f"Data saved successfully: {result}", "SUCCESS")
            return True
        else:
            print_status(f"Failed to save data: {response.text}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error saving data: {e}", "ERROR")
        return False

def test_load_data():
    """Test loading data from the server"""
    print_status("Testing data load...", "INFO")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/shared-data/{TEST_TAB_ID}",
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print_status(f"Data loaded successfully", "SUCCESS")
            print_status(f"Data: {json.dumps(result, indent=2)}", "INFO")
            return True
        else:
            print_status(f"Failed to load data: {response.text}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error loading data: {e}", "ERROR")
        return False

def test_all_data():
    """Test getting all shared data"""
    print_status("Testing get all data...", "INFO")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/shared-data",
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            print_status(f"All data retrieved successfully", "SUCCESS")
            print_status(f"Number of tabs with data: {len([k for k in result.get('data', {}).keys() if not k.endswith('_timestamp') and not k.endswith('_user')])}", "INFO")
            return True
        else:
            print_status(f"Failed to get all data: {response.text}", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error getting all data: {e}", "ERROR")
        return False

def test_collaborative_sync():
    """Test the collaborative sync by simulating two users"""
    print_status("Testing collaborative sync simulation...", "INFO")
    
    # User 1 saves data
    user1_data = {
        "data": {"0": "User1 Value", "1": "Working fine"},
        "user": "User 1"
    }
    
    try:
        response1 = requests.post(
            f"{API_BASE_URL}/shared-data/testTab",
            json=user1_data,
            timeout=5
        )
        
        if response1.status_code != 200:
            print_status("User 1 failed to save", "ERROR")
            return False
        
        print_status("User 1 saved data", "SUCCESS")
        
        # Wait a moment
        time.sleep(0.5)
        
        # User 2 loads data
        response2 = requests.get(
            f"{API_BASE_URL}/shared-data/testTab",
            timeout=5
        )
        
        if response2.status_code != 200:
            print_status("User 2 failed to load", "ERROR")
            return False
        
        loaded_data = response2.json()
        
        # Verify User 2 got User 1's data
        if loaded_data.get('data', {}).get('0') == "User1 Value":
            print_status("User 2 successfully received User 1's data!", "SUCCESS")
            print_status("Collaborative sync is working correctly", "SUCCESS")
            return True
        else:
            print_status("Data mismatch - sync may not be working", "ERROR")
            return False
            
    except Exception as e:
        print_status(f"Error in collaborative sync test: {e}", "ERROR")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print(" Collaborative Live Report - Test Suite")
    print("="*60 + "\n")
    
    tests = [
        ("Health Check", test_health_check),
        ("Save Data", test_save_data),
        ("Load Data", test_load_data),
        ("Get All Data", test_all_data),
        ("Collaborative Sync", test_collaborative_sync)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"Test crashed: {e}", "ERROR")
            results.append((test_name, False))
        time.sleep(0.5)
    
    # Summary
    print("\n" + "="*60)
    print(" Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        color = "SUCCESS" if result else "ERROR"
        print_status(f"{status}: {test_name}", color)
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print_status("\n🎉 All tests passed! Collaborative sync is ready to use.", "SUCCESS")
    else:
        print_status("\n⚠️  Some tests failed. Check the errors above.", "WARNING")
        print_status("Make sure the API server is running: python api_server.py", "INFO")
    
    print("\n")

if __name__ == "__main__":
    main()
