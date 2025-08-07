#!/usr/bin/env python3
"""
Test script to verify Docker setup
This helps ensure the Dockerfile and application will work in containerized environment
"""

import os
import sys

def test_environment():
    """Test if we're in a containerized environment"""
    print("Testing environment...")
    
    # Check if we're in a container
    if os.path.exists('/.dockerenv'):
        print("✅ Running in Docker container")
    else:
        print("ℹ️  Running in local environment")
    
    # Check Python path
    python_path = os.environ.get('PYTHONPATH', 'Not set')
    print(f"✅ PYTHONPATH: {python_path}")
    
    # Check working directory
    cwd = os.getcwd()
    print(f"✅ Working directory: {cwd}")
    
    # Check if src directory exists
    src_path = os.path.join(cwd, 'src')
    if os.path.exists(src_path):
        print("✅ src directory found")
    else:
        print("❌ src directory not found")
        return False
    
    return True

def test_imports():
    """Test if we can import the application"""
    print("\nTesting imports...")
    
    try:
        # Add src to path
        src_path = os.path.join(os.getcwd(), 'src')
        sys.path.insert(0, src_path)
        
        # Test basic imports
        import api.main
        print("✅ Successfully imported api.main")
        
        # Test app creation
        app = api.main.app
        print("✅ Successfully created FastAPI app")
        
        # Test health endpoint
        from fastapi.testclient import TestClient
        client = TestClient(app)
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
            
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    print("🐳 Docker Setup Test")
    print("=" * 50)
    
    # Test environment
    if not test_environment():
        print("❌ Environment test failed")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Docker setup looks good.")
    print("You can now deploy to Render using the Dockerfile.")

if __name__ == "__main__":
    main()
