import client
import json

def handle_message(sock, data):
    try:
        # Parse the message
        msg = json.loads(data)
        msg_type = msg.get("type")
        msg_data = msg.get("data")
        
        if msg_type == "join_broadcast":
            print(f"\nPlayer {msg_data['username']} has joined the game.")
       
    except json.JSONDecodeError:
        print(f"Failed to decode message: {data}") 