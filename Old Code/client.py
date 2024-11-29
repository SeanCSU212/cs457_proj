import socket
import json
import threading
import argparse

'''ARGUMENT HANDLING FOR STARTING CLIENT PROGRAM'''

parser = argparse.ArgumentParser(
    description = "Welcome to the Tic-Tac-Toe-Two Client! \nUSAGE: python3 client.py -i <Server IP> -p <port>",
    epilog = "HOW TO PLAY: \n\n 1. Wait for 3 players to connect \n 2. Wait for your turn, the server will message you when it is your turn \n 3. Upon your turn, enter the MOVE command, followed by the 2 character letter-number combo of the space you want tot move to. \n(Players can only play on spaces that have not yet been played on) \n4. The first player to get 3 in a row (vertically, horizontally, or diagonally) Wins! \n\n GOOD LUCK!",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('-i', '--serveraddress', type=str, required=True, help='Server IP Address')
parser.add_argument('-p', '--port', type=str, required=True, help='Port Number')
parser.add_argument('-n', '--dns', type=str, )

args = parser.parse_args()


host = args.serveraddress
port = int(args.port)

active_turn = False

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.sendall(message.encode()) 

def handle_server_response(sock):
    buffer = b""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("Server closed the connection")
                break
            buffer += data
            try:
                message = json.loads(buffer.decode())
                process_message(message)
                buffer = b""  # Clear the buffer after successfully processing a message
            except json.JSONDecodeError:
                continue  # Keep reading until we have a complete message
        except (json.JSONDecodeError) as e:
            print(f"Error receiving or parsing server response: {e}")
            break

def process_message(message):
    global active_turn
    msg_type = message["type"]
    if msg_type == "join_broadcast":
        handle_join_broadcast(message["data"])
    elif msg_type == "chat_broadcast":
        handle_chat_broadcast(message["data"])
    elif msg_type == "quit_broadcast":
        handle_quit_broadcast(message["data"])
    elif msg_type == "start_broadcast":
        handle_start_broadcast(message["data"]) 
    elif msg_type == "gameboard_broadcast":
        handle_gameboard_broadcast(message["data"])
    elif msg_type == "activate_turn":
        active_turn = True
        print("Your turn...")
    elif msg_type == "deactivate_turn":
        active_turn = False
    

def handle_gameboard_broadcast(data):
    print(f"\n Current Game Board: \n{data['game_board']}")

def handle_start_broadcast(data):
    print (f"\n3 Players Joined... Starting Game!")

def handle_join_broadcast(data):
    print(f"\nPlayer {data['username']} with piece {data['player']} has joined the game.")

def handle_chat_broadcast(data):
    print(f"\nChat from {data['sender_id']}: {data['message']}")

def handle_quit_broadcast(data):
    print(f"\nPlayer {data['player']} has quit the game.")





def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        threading.Thread(target=handle_server_response, args=(sock,)).start()
        
       #PROMPT USER FOR NAME FOLLOWING CLIENT SETUP
        username = input("Enter username: ")
        send_message(sock, "join", {"username": username})

        #SET CLIENTS PLAY STATE TO FALSE
        global active_turn

        while True:

            if (active_turn):
                position = input("Enter # of position you want play on: ").strip()
                send_message(sock, "move", {"position": position})

            else:
                command = input("Enter command (chat/quit): ").strip()
                if command == "chat":
                    message = input("Enter chat message: ").strip()
                    send_message(sock, "chat", {"message": message, "username": username})
                elif command == "quit":
                    send_message(sock, "quit", {})
                    break

if __name__ == "__main__":
    main()
