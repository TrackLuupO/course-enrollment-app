import requests

BASE_URL = "http://localhost:8000"

def main():
    print("🚀 Starting API tests...")
    
    endpoints = [
        ("GET", "/", "Root endpoint"),
        ("GET", "/health", "Health check"),
        ("GET", "/students/", "Get all students"),
        ("GET", "/courses/", "Get all courses"),
        ("GET", "/stats/", "Get statistics"),
    ]
    
    all_passed = True
    
    for method, endpoint, description in endpoints:
        print(f"\n📡 Testing {description} ({method} {endpoint})...")
        try:
            if method == "GET":
                response = requests.get(BASE_URL + endpoint, timeout=5)
            elif method == "POST":
                response = requests.post(BASE_URL + endpoint, timeout=5)
            
            if 200 <= response.status_code < 300:
                print(f"   ✅ Success! Status: {response.status_code}")
                if endpoint in ["/students/", "/courses/"]:
                    data = response.json()
                    count = len(data)
                    print(f"   📊 Found {count} items")
            else:
                print(f"   ❌ Failed! Status: {response.status_code}")
                print(f"   Response: {response.text}")
                all_passed = False
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Cannot connect to {BASE_URL}")
            print(f"   Make sure the server is running: uvicorn main:app --reload --port 8000")
            all_passed = False
            break
        except Exception as e:
            print(f"   ❌ Error: {e}")
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! API is working correctly.")
        print("\n📋 Quick manual tests you can try:")
        print("   1. Open http://localhost:8000/docs in your browser for Swagger UI")
        print("   2. Try creating a new student: POST /students/")
        print("   3. Try creating a new course: POST /courses/")
        print("   4. Try enrolling a student: POST /enrollments/")
    else:
        print("\n❌ Some tests failed. Check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
