#!/usr/bin/env python3
"""
Test script to verify backend deployment
Run this after deploying to Render to check if everything is working
"""

import requests
import sys
import os

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health endpoint working")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_docs_endpoint(base_url):
    """Test the docs endpoint"""
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("✅ Docs endpoint working")
            return True
        else:
            print(f"❌ Docs endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Docs endpoint error: {e}")
        return False

def test_cors_headers(base_url):
    """Test CORS headers"""
    try:
        response = requests.options(f"{base_url}/health", timeout=10)
        cors_headers = response.headers.get('Access-Control-Allow-Origin')
        if cors_headers:
            print(f"✅ CORS headers present: {cors_headers}")
            return True
        else:
            print("❌ CORS headers missing")
            return False
    except Exception as e:
        print(f"❌ CORS test error: {e}")
        return False

def main():
    # Get base URL from command line or use default
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    else:
        base_url = input("Enter your Render backend URL (e.g., https://your-app.onrender.com): ").rstrip('/')
    
    if not base_url:
        print("❌ No URL provided")
        sys.exit(1)
    
    print(f"Testing backend at: {base_url}")
    print("-" * 50)
    
    # Run tests
    tests = [
        test_health_endpoint,
        test_docs_endpoint,
        test_cors_headers
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test(base_url):
            passed += 1
        print()
    
    print("-" * 50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your backend is ready.")
    else:
        print("⚠️  Some tests failed. Check your deployment.")
        sys.exit(1)

if __name__ == "__main__":
    main()
