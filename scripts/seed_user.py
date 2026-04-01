import requests
import json
import time
import asyncio

BASE_URL = "http://localhost:8000"

USERS = [
    {"username": "amit_sharma", "email": "amit@example.com", "password": "password123"},
    {"username": "priya_patel", "email": "priya@example.com", "password": "password123"},
    {"username": "raj_kumar", "email": "raj@example.com", "password": "password123"},
    {"username": "neha_singh", "email": "neha@example.com", "password": "password123"},
    {"username": "vikram_reddy", "email": "vikram@example.com", "password": "password123"},
    {"username": "anita_desai", "email": "anita@example.com", "password": "password123"},
    {"username": "suresh_iyer", "email": "suresh@example.com", "password": "password123"},
    {"username": "kavita_nair", "email": "kavita@example.com", "password": "password123"},
    {"username": "arjun_mehta", "email": "arjun@example.com", "password": "password123"},
    {"username": "divya_joshi", "email": "divya@example.com", "password": "password123"},
]

def wait_for_server():
    """Wait for server to be ready"""
    for i in range(10):
        try:
            response = requests.get(f"{BASE_URL}/health")
            if response.status_code == 200:
                print("✅ Server ready")
                return True
        except:
            print(f"Waiting for server... ({i+1}/10)")
            time.sleep(2)
    return False

def seed_users():
    """Create test users"""
    tokens = {}
    
    for user in USERS:
        # Register
        resp = requests.post(f"{BASE_URL}/api/auth/register", json=user)
        if resp.status_code == 201:
            print(f"✅ Created: {user['username']}")
        elif resp.status_code == 400:
            print(f"⚠️  Exists: {user['username']}")
        
        # Login
        resp = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={"username": user["username"], "password": user["password"]}
        )
        
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            tokens[user["username"]] = token
            print(f"🔑 Token: {user['username']}")
    
    # Save tokens
    with open("user_tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)
    
    print(f"\n✅ Created {len(tokens)} users")
    return tokens

if __name__ == "__main__":
    print("🔍 Seeding database...")
    if wait_for_server():
        seed_users()
    else:
        print("❌ Server not running")