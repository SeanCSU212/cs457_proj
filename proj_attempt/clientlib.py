import client
import json

def handle_message(sock, data):
    try:
        # Parse the message
        msg = json.loads(data)
        msg_type = msg.get("type")
        msg_data = msg.get("data")
        
        # Handling for join broadcast
        if msg_type == "join_broadcast":
            print(f"\nPlayer {msg_data['username']} has joined the game.")

        # Handling for game start
        if msg_type == "start_game":
            print(f"\n3 Player joined! Starting game...\nWelcome to Tic-Tac-Toe-Two!\n")
       
        # Handling for display board
        if msg_type == 'display_board':
            print(f"Current Game Board: \n{msg_data['board']}")
            
    except json.JSONDecodeError:
        print(f"Failed to decode message: {data}") 