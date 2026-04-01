import requests
import json

BASE_URL = "http://localhost:8000"

# Test users
users = [
    {"username": "alice", "email": "alice@example.com", "password": "alice123"},
    {"username": "bob", "email": "bob@example.com", "password": "bob123"},
    {"username": "charlie", "email": "charlie@example.com", "password": "charlie123"},
]

def create_users():
    """Create test users"""
    tokens = {}
    
    for user in users:
        # Register
        print(f"\n📝 Registering {user['username']}...")
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=user
        )
        
        if response.status_code == 201:
            print(f"✅ Created: {user['username']}")
        elif response.status_code == 400:
            print(f"⚠️  Already exists: {user['username']}")
        else:
            print(f"❌ Failed: {response.text}")
            continue
        
        # Login
        print(f"🔑 Logging in {user['username']}...")
        login_response = requests.post(
            f"{BASE_URL}/api/auth/login",
            data={
                "username": user["username"],
                "password": user["password"]
            }
        )
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            tokens[user["username"]] = token
            print(f"✅ Token obtained for {user['username']}")
        else:
            print(f"❌ Login failed: {login_response.text}")
    
    # Save tokens
    with open("tokens.json", "w") as f:
        json.dump(tokens, f, indent=2)
    
    print(f"\n🎉 Successfully created {len(tokens)} users")
    print("\nUser IDs (for WebSocket connections):")
    for i, username in enumerate(tokens.keys(), 1):
        print(f"  {i}. {username} (ID: {i})")
    
    return tokens

def send_test_message():
    """Send a test message between users"""
    try:
        with open("tokens.json", "r") as f:
            tokens = json.load(f)
        
        if len(tokens) < 2:
            print("Need at least 2 users to send messages")
            return
        
        users_list = list(tokens.keys())
        sender = users_list[0]
        receiver = users_list[1]
        
        print(f"\n💬 Sending test message from {sender} to {receiver}...")
        
        response = requests.post(
            f"{BASE_URL}/api/messages/send",
            headers={"Authorization": f"Bearer {tokens[sender]}"},
            json={
                "content": "Hello! This is a test message from the chat app!",
                "receiver_id": 2  # Assuming receiver ID is 2
            }
        )
        
        if response.status_code == 201:
            print("✅ Message sent successfully!")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Failed: {response.text}")
            
    except FileNotFoundError:
        print("No tokens found. Run create_test_users.py first")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("🚀 Setting up test users...")
    tokens = create_users()
    
    if tokens:
        send_test_message()