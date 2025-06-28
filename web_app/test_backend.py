#!/usr/bin/env python3
"""
Simple test script to verify the PBIL backend API is working correctly.
"""

import requests
import time
import json

# Test configuration
BASE_URL = "http://localhost:8000"

def test_api_status():
    """Test the API status endpoint."""
    print("🔍 Testing API status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Status: {data}")
            return True
        else:
            print(f"❌ API Status failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Status error: {e}")
        return False

def test_cnf_files():
    """Test the CNF files listing endpoint."""
    print("\n📁 Testing CNF files listing...")
    try:
        response = requests.get(f"{BASE_URL}/api/cnf-files")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ CNF Files: {data}")
            return True
        else:
            print(f"❌ CNF Files failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ CNF Files error: {e}")
        return False

def test_pbil_run():
    """Test running PBIL algorithm."""
    print("\n🧬 Testing PBIL run...")
    try:
        config = {
            "cnf_file": "sample_problem.cnf",
            "pop_size": 50,
            "learning_rate": 0.1,
            "negative_learning_rate": 0.075,
            "mutation_probability": 0.02,
            "mutation_shift": 0.05,
            "max_iterations": 100
        }
        
        response = requests.post(f"{BASE_URL}/api/pbil/run", json=config)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ PBIL Run: {data.get('result', {}).get('fitness', 'N/A')}/{data.get('result', {}).get('max_fitness', 'N/A')} fitness")
            return True
        else:
            print(f"❌ PBIL Run failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ PBIL Run error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing PBIL Backend API")
    print("=" * 40)
    
    # Give the server a moment to start if just launched
    time.sleep(2)
    
    # Run tests
    tests = [
        test_api_status,
        test_cnf_files,
        test_pbil_run
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
        print(f"\n🌐 You can now access:")
        print(f"   • API docs: {BASE_URL}/docs")
        print(f"   • WebSocket: ws://localhost:8000/ws/pbil")
        print(f"   • Frontend: Start with 'npm start' in the frontend directory")
    else:
        print("⚠️  Some tests failed. Check the backend logs.")

if __name__ == "__main__":
    main() 