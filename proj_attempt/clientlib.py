import client
import json


def handle_message(sock, data):
    try:
        #print(data) #print entire message data  for debugging
        # Parse the message
        msg = json.loads(data)
        msg_type = msg.get("type")
        msg_data = msg.get("data")
        
        # Handling for join broadcast
        if msg_type == "join_broadcast":
            print(f"\nPlayer {msg_data['username']} has joined the game.")

        # Handling for game start
        elif msg_type == "start_game":
            print(f"\n3 Player joined! Starting game...\nWelcome to Tic-Tac-Toe-Two!\nCurrent Game Board: \n {msg_data['board']}")
       
        # Handling for display board
        elif msg_type == "display_board":
            print(f"Current Game Board: \n{msg_data['board']}")
       
        # Handling for turn input
        elif msg_type == "your_turn":
            move = input("\nEnter move (1-16): ")
            client.send_message(sock, "make_move", {"move": move})

        # Handling for moves made by other players
        elif msg_type == 'move_broadcast':
            print(f"\n{msg_data['player']} placed a piece of position {msg_data['move']}")     

        # Handling for invalid move
        elif msg_type == "invalid_move":
            print(f"\n Invalid Move, cannot place piece on positon {msg_data['move']}... Try again.")

        # Handling for game_over
        elif msg_type == "game_over":
            print(f"GAME OVER! {msg_data['winner']} won the game!")

    except json.JSONDecodeError:
        print(f"Failed to decode message: {data}") 