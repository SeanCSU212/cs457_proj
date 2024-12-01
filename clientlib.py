import client
import json
import sys


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
        elif msg_type == "start_game":
            print(f"\n3 Player joined! Starting game..." +
                  f"\n\nWelcome to " +
                  f"\n  _____ _         _____             _____              _____               " +
                  f"\n |_   _(_) ___   |_   _|_ _  ___   |_   _|__   ___    |_   _|_      _____  " +
                  f"\n   | | | |/ __|____| |/ _` |/ __|____| |/ _ \ / _ \_____| | \ \ /\ / / _ \ " +
                  f"\n   | | | | (_|_____| | (_| | (_|_____| | (_) |  __/_____| |  \ V  V / (_) |" +
                  f"\n   |_| |_|\___|    |_|\__,_|\___|    |_|\___/ \___|     |_|   \_/\_/ \___/ " +
                  f"\n                                                                           " +
                  f" \nHow to play: \n1. Wait for the server to prompt your turn \n2. Upon your turn, enter the number of the position you want to play your piece \n3. Be the first to place 3 pieces in a row (vertically, horizontally, or diagonally) to win!" +
                  f"\n\nGood Luck!\n\n" +
                  f"\nCurrent Game Board: \n\n{msg_data['board']}\n")
       
        # Handling for display board
        elif msg_type == "display_board":
            print(f"Current Game Board: \n\n{msg_data['board']}\n")
       
        # Handling for turn input
        elif msg_type == "your_turn":
            move = input("\nEnter move (1-16): ")
            client.send_message(sock, "make_move", {"move": move})

        # Handling for moves made by other players
        elif msg_type == 'move_broadcast':
            print(f"\n{msg_data['player']} placed a piece on position {msg_data['move']}")     

        # Handling for invalid move
        elif msg_type == "invalid_move":
            print(f"\n Invalid Move, cannot place piece on positon {msg_data['move']}... Try again.")

        # Handling for game_over with winner
        elif msg_type == "game_over_win":
            print(f"GAME OVER! {msg_data['winner']} won the game!")
        
        # Handling for game_over from draw
        elif msg_type == "game_over_draw":
            print(f"GAME OVER! No winner...")
        
        # Handling for end of game
        elif msg_type == "play_again":
            end_of_game(sock)
            


    except json.JSONDecodeError:
        print(f"Failed to decode message: {data}") 

def end_of_game(sock):
    choice = input("Do you want to play again or quit? (type 'play' to play again or 'quit' to exit): ").strip().lower()
    if choice == 'play':
        username = input("Enter Username: ")
        client.send_message(sock, "join", {"username": username})
    elif choice == 'quit':
        print("\nLeaving game...")
        sys.exit()
    else:
        end_of_game()
