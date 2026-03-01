"""
Test FastAPI health without database connection
"""
import sys
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Create test app
app = FastAPI(title="EduNexus API Health Test")

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is working!"}

@app.get("/test")
def test():
    return {"test": "success", "imports": "working"}

if __name__ == "__main__":
    print("✅ FastAPI imports successful!")
    print("✅ Starting test server...")
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
