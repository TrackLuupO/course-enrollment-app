import requests
import time

print("🚀 Initializing Course Enrollment System...")
print("📡 Testing backend connection...")

# Wait for backend to start
time.sleep(2)

BASE_URL = "http://localhost:8000"

# Test connection
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"✅ Backend is running: {response.status_code}")
    
    # Test API endpoints
    endpoints = [
        ("/", "Root"),
        ("/students/", "Students"),
        ("/courses/", "Courses"),
        ("/stats/", "Statistics")
    ]
    
    for endpoint, name in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}")
        print(f"  {name}: {'✅' if response.status_code == 200 else '❌'} {response.status_code}")
    
    print("\n🎉 System is ready!")
    print("🌐 Frontend: http://localhost:8082")
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    
except requests.exceptions.ConnectionError:
    print("❌ Cannot connect to backend. Make sure it's running:")
    print("   cd backend && uvicorn main:app --reload --port 8000")