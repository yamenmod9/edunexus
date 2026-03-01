"""
Quick Backend Test Script
Run this to verify the backend is working
"""
import requests
import sys

def test_backend():
    base_url = "http://localhost:8000"

    print("🧪 Testing EduNexus Backend...")
    print("=" * 50)

    # Test 1: Health endpoint
    try:
        response = requests.get(f"{base_url}/api/health", timeout=3)
        if response.status_code == 200:
            print("✅ Health endpoint: WORKING")
        else:
            print(f"❌ Health endpoint: Got status {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Health endpoint: Cannot connect - is backend running?")
        print("\n📝 To start backend, run:")
        print("   cd backend")
        print("   venv\\Scripts\\activate")
        print("   python -m uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Health endpoint: Error - {e}")
        sys.exit(1)

    # Test 2: Root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=3)
        if response.status_code == 200:
            print("✅ Root endpoint: WORKING")
            data = response.json()
            print(f"   Version: {data.get('version', 'unknown')}")
        else:
            print(f"❌ Root endpoint: Got status {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint: Error - {e}")

    # Test 3: Mistakes endpoints
    print("\n🔍 Checking Mistakes API routes...")

    # Get docs to see available routes
    try:
        response = requests.get(f"{base_url}/openapi.json", timeout=3)
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get('paths', {})

            mistakes_routes = [path for path in paths.keys() if 'mistakes' in path]

            if mistakes_routes:
                print(f"✅ Found {len(mistakes_routes)} mistakes routes:")
                for route in mistakes_routes:
                    print(f"   - {route}")
            else:
                print("❌ No mistakes routes found!")
                print("   Expected routes:")
                print("   - /api/mistakes")
                print("   - /api/mistakes/stats")
                print("   - /api/mistakes/count")
        else:
            print(f"❌ Cannot get OpenAPI spec: {response.status_code}")
    except Exception as e:
        print(f"❌ Error checking routes: {e}")

    print("\n" + "=" * 50)
    print("✅ Backend test complete!")
    print("\n📋 Next steps:")
    print("   1. Check that 'EduNexus Backend Server' window shows no errors")
    print("   2. Visit http://localhost:8000/docs to see API documentation")
    print("   3. The Flutter app should now connect successfully")

if __name__ == "__main__":
    test_backend()
