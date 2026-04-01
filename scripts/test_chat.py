import requests
import json
import time
import random

BASE_URL = "http://localhost:8000"

# Load tokens
try:
    with open("user_tokens.json", "r") as f:
        tokens = json.load(f)
except FileNotFoundError:
    print("❌ user_tokens.json not found. Run seed_users.py first!")
    exit(1)

usernames = list(tokens.keys())
user_ids = {username: idx + 1 for idx, username in enumerate(usernames)}

def get_user_id(username):
    return user_ids[username]

def send_message(sender, receiver, message):
    """Send a message via REST API"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/messages/send",
            headers={"Authorization": f"Bearer {tokens[sender]}"},
            json={
                "content": message,
                "receiver_id": get_user_id(receiver)
            }
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def simulate_conversation():
    """Simulate random conversations between users"""
    print("Starting chat simulation...")
    print(f"Users: {', '.join(usernames)}")
    print("Press Ctrl+C to stop\n")
    
    message_templates = [
        "Hey, how are you?",
        "Did you see the latest update?",
        "Working on the project?",
        "Let's meet tomorrow",
        "Check out the new feature",
        "Nice work!",
        "Any updates?",
        "I'll share the docs",
        "Thanks for the help!",
        "Good morning!",
        "What's up?",
        "Are you free later?",
        "Just finished the code",
        "Looks good to me",
        "Can you review this?"
    ]
    
    while True:
        # Pick random users
        sender = random.choice(usernames)
        receiver = random.choice([u for u in usernames if u != sender])
        
        message = random.choice(message_templates)
        
        if send_message(sender, receiver, message):
            print(f"📨 {sender} -> {receiver}: {message}")
        else:
            print(f"❌ Failed to send from {sender} to {receiver}")
        
        # Wait 3-8 seconds between messages
        time.sleep(random.uniform(3, 8))

if __name__ == "__main__":
    try:
        simulate_conversation()
    except KeyboardInterrupt:
        print("\n\n✅ Simulation stopped")
        print(f"Total messages sent between {len(usernames)} users")