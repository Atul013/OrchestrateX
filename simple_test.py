import requests

try:
    r = requests.get('http://localhost:8002/status', timeout=5)
    print(f"API Status: {r.status_code}")
    if r.status_code == 200:
        print("✅ API is running!")
        print("Now test with frontend...")
except:
    print("❌ API not responding")
