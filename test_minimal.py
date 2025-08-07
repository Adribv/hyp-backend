#!/usr/bin/env python3
"""
Minimal test to verify FastAPI app can start
This helps isolate whether the issue is with the app itself or database initialization
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from api.main import app
    print("✅ Successfully imported FastAPI app")
    
    # Test basic app functionality
    print(f"✅ App title: {app.title}")
    print(f"✅ App version: {app.version}")
    print(f"✅ App description: {app.description}")
    
    # Check if health endpoint exists
    routes = [route.path for route in app.routes]
    if "/health" in routes:
        print("✅ Health endpoint found in routes")
    else:
        print("❌ Health endpoint not found in routes")
    
    print("✅ Minimal test passed - app can be imported successfully")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
