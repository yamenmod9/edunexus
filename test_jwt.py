"""Test JWT token creation and validation"""
import sys
sys.path.insert(0, '.')

from app.core.security import create_access_token, decode_token
from jose import jwt, JWTError
from app.core.config import settings

# Create a test token with string sub (JWT standard)
test_data = {"sub": "123"}
token = create_access_token(test_data)
print(f"Created token: {token[:50]}...")

# Try to decode it directly with jose
print(f"\nTrying to decode with jose directly...")
print(f"SECRET_KEY: {settings.SECRET_KEY[:20]}...")
print(f"ALGORITHM: {settings.ALGORITHM}")

try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print(f"✅ Direct decode successful: {payload}")
except JWTError as e:
    print(f"❌ JWT Error: {e}")
except Exception as e:
    print(f"❌ Other Error: {e}")

# Try with our function
decoded = decode_token(token)
print(f"\nUsing decode_token function: {decoded}")

if decoded:
    print("✅ Token validation works!")
else:
    print("❌ Token validation failed!")
