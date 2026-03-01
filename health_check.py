"""
Backend Health Check Script
Tests all components without requiring database
"""

print("=" * 60)
print("🏥 EduNexus Backend Health Check")
print("=" * 60)
print()

# Test 1: Python version
print("[1/8] Checking Python version...")
import sys
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
print(f"✅ Python {python_version}")
print()

# Test 2: Core dependencies
print("[2/8] Testing core dependencies...")
try:
    import fastapi
    print(f"✅ FastAPI {fastapi.__version__}")
except ImportError as e:
    print(f"❌ FastAPI import failed: {e}")
    sys.exit(1)

try:
    import flask
    print(f"✅ Flask {flask.__version__}")
except ImportError as e:
    print(f"❌ Flask import failed: {e}")
    sys.exit(1)

try:
    import sqlalchemy
    print(f"✅ SQLAlchemy {sqlalchemy.__version__}")
except ImportError as e:
    print(f"❌ SQLAlchemy import failed: {e}")
    sys.exit(1)

try:
    import pydantic
    print(f"✅ Pydantic {pydantic.__version__}")
except ImportError as e:
    print(f"❌ Pydantic import failed: {e}")
    sys.exit(1)

print()

# Test 3: Security modules
print("[3/8] Testing security modules...")
try:
    from passlib.context import CryptContext
    print("✅ Passlib (password hashing)")
except ImportError as e:
    print(f"❌ Passlib import failed: {e}")
    sys.exit(1)

try:
    from jose import jwt
    print("✅ Python-JOSE (JWT)")
except ImportError as e:
    print(f"❌ Python-JOSE import failed: {e}")
    sys.exit(1)

print()

# Test 4: Core configuration
print("[4/8] Testing core configuration...")
try:
    from app.core.config import settings
    print(f"✅ Settings loaded")
    print(f"   - Environment: {settings.ENVIRONMENT}")
    print(f"   - FastAPI Port: {settings.FASTAPI_PORT}")
    print(f"   - Flask Port: {settings.FLASK_PORT}")
except Exception as e:
    print(f"❌ Config failed: {e}")
    sys.exit(1)

print()

# Test 5: Security functions
print("[5/8] Testing security functions...")
try:
    from app.core.security import get_password_hash, verify_password, create_access_token

    # Test password hashing
    test_password = "test123"
    hashed = get_password_hash(test_password)
    if verify_password(test_password, hashed):
        print("✅ Password hashing/verification")
    else:
        print("❌ Password verification failed")
        sys.exit(1)

    # Test JWT creation
    token = create_access_token(data={"sub": 1})
    if token and len(token) > 10:
        print("✅ JWT token generation")
    else:
        print("❌ JWT token generation failed")
        sys.exit(1)

except Exception as e:
    print(f"❌ Security functions failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 6: Models (without database)
print("[6/8] Testing model definitions...")
try:
    from app.models import User, Question, PracticeSession, Test
    print("✅ User model")
    print("✅ Question model")
    print("✅ PracticeSession model")
    print("✅ Test model")
except Exception as e:
    print(f"❌ Model import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 7: Schemas
print("[7/8] Testing Pydantic schemas...")
try:
    from app.schemas import UserCreate, QuestionResponse, PracticeSessionStart

    # Test schema validation
    user = UserCreate(email="test@example.com", password="password123")
    print("✅ UserCreate schema")

    session = PracticeSessionStart(topics=["Algebra", "Geometry"])
    print("✅ PracticeSessionStart schema")

except Exception as e:
    print(f"❌ Schema validation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()

# Test 8: FastAPI app creation
print("[8/8] Testing FastAPI application...")
try:
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    # Create minimal test app
    test_app = FastAPI()

    @test_app.get("/test")
    def test_endpoint():
        return {"status": "ok"}

    client = TestClient(test_app)
    response = client.get("/test")

    if response.status_code == 200 and response.json()["status"] == "ok":
        print("✅ FastAPI app creation and routing")
    else:
        print("❌ FastAPI test failed")
        sys.exit(1)

except Exception as e:
    print(f"❌ FastAPI test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✅ ALL HEALTH CHECKS PASSED!")
print("=" * 60)
print()
print("⚠️  Note: Database connectivity not tested (PostgreSQL not required yet)")
print()
print("Next steps:")
print("1. Install PostgreSQL if you want full database functionality")
print("2. Or use SQLite for testing: Update DATABASE_URL in .env")
print("3. Run: python app/main.py (to start FastAPI)")
print("4. Run: python flask_app.py (to start Flask admin)")
print()
print("For SQLite testing, change .env to:")
print("DATABASE_URL=sqlite:///./edunexus.db")
print()
