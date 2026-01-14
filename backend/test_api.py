import requests
import json

URL = "https://insight-portal-hoxx.onrender.com"
EMAIL = "test_connectivity_user_99@example.com"
PASSWORD = "password123"

print("Testing Registration Endpoint...")
print("-" * 50)

endpoint = f"{URL}/auth/register"
payload = {
    "email": EMAIL,
    "password": PASSWORD,
    "full_name": "Test User",
    "role": "client"
}

try:
    r = requests.post(endpoint, json=payload, timeout=15)
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
    
    if r.status_code == 200:
        print("\nSUCCESS: Registration worked!")
    elif r.status_code == 400 and "already registered" in r.text:
         print("\nSUCCESS: Endpoint reachable (User already exists).")
    else:
        print(f"\nFAILED: API Error: {r.status_code}")
        print(f"Details: {r.text}")

except Exception as e:
    print(f"\nFAILED: Network Error: {e}")

print("-" * 50)
