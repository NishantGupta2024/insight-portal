import requests
import time

URL = "https://insight-portal-hoxx.onrender.com"
ORIGIN = "https://gleaming-fudge-1e4b0c.netlify.app"

print(f"Diagnostics starting for: {URL}")
print("-" * 50)

# 1. Check Root Availability
try:
    print(1, "Checking Server Reachability...")
    start = time.time()
    r = requests.get(URL, timeout=10)
    print(f"   Success! Status: {r.status_code} (Time: {time.time()-start:.2f}s)")
except Exception as e:
    print(f"   FAILED to connect: {e}")

# 2. Check CORS Headers (Preflight)
print("\n2. Checking CORS Headers (OPTIONS request)...")
try:
    headers = {
        "Origin": ORIGIN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    }
    r = requests.options(f"{URL}/auth/login", headers=headers, timeout=10)
    
    print(f"   Status: {r.status_code}")
    print(f"   Access-Control-Allow-Origin: {r.headers.get('access-control-allow-origin', 'MISSING')}")
    print(f"   Access-Control-Allow-Methods: {r.headers.get('access-control-allow-methods', 'MISSING')}")
    
    if r.headers.get('access-control-allow-origin') == ORIGIN:
        print("   ✅ CORS Configured Correctly!")
    else:
        print("   ❌ CORS HEADER MISSING OR WRONG")

except Exception as e:
    print(f"   FAILED to check CORS: {e}")

print("-" * 50)
