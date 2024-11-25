import socket
import selectors
import types
import argparse
import json
import serverlib
from game import *


sel = selectors.DefaultSelector()
players = []
player_data = {}
turn_index = 0

def accept_wrapper(sock):
    try:
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}") # Log connection from client
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, data=types.SimpleNamespace(addr=addr))
        #players.append(conn) # Add socket to list of players 
        #conn.sendall(f"Welcome player {len(players)}\n".encode()) # Send welcome message to clients

        #if len(players) == 3:
            #start_game()

    except socket.timeout:
        print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds") # type: ignore
    except socket.error as e:
        print(f"Socket error: {e}")

def start_game():
    broadcast("start_game", None) # Broadcast starting game message to all Clients
    broadcast("display_board", {"board": display_board()}) # Broadcast empty game board to all clients
    send_message(players[turn_index], "your_turn", None)


'''def start_game():
    for player in players:
        player.sendall("Game started! Here is the board:\n".encode())
        player.sendall(display_board().encode())
    players[turn_index].send("It's your turn!\n".encode())
'''
#Handles connections and game logic
def service_connection(key, mask):
    global turn_index
    sock = key.fileobj
    data = key.data 

    if mask & selectors.EVENT_READ:
        message = sock.recv(1024).decode('utf-8').strip()
        if message:
            try:
                serverlib.handle_message(sock, data, message)
                '''
                move = int(data)
                if check_move_legality(move):
                    make_move(move, ' X' if turn_index == 0 else ' O' if turn_index == 1 else ' +')
                    broadcast(f"Player {turn_index + 1} made a move.\n{display_board()}")
                    if is_over():
                        #broadcast(players[turn_index], " has won. Game over!")
                        sel.unregister(sock)
                        sock.close()
                    else:
                        turn_index = (turn_index + 1) % 3
                        players[turn_index].sendall("It's your turn!\n".encode())
                else:
                    sock.sendall("Illegal move. Try again.\n".encode())
                    sock.sendall("It's your turn!\n".encode())
            except ValueError:
                sock.sendall("Invalid input. Enter a number between 1 and 16.\n".encode())
            '''
            except socket.timeout:
                print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
            except socket.error as e:
                print(f"Socket error while receiving communication: {e}")
 
def broadcast(msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    for client_socket in player_data:
        client_socket.send(message.encode())

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.send(message.encode())

def main():
    # Handling for Arguments
    parser = argparse.ArgumentParser(description = "Welcome to the Tic-Tac-Toe-Two Server! \nUSAGE: python3 server.py -p <port>")
    parser.add_argument('-p', '--port', type=str, required=True, help='Port Number')
    args = parser.parse_args()
    host = '0.0.0.0' # Set static listening IP
    port = int(args.port)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((host, port))
    server_sock.listen()
    server_sock.setblocking(False)
    sel.register(server_sock, selectors.EVENT_READ, data=None)

    print(f"Server running on {host}:{port}")

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        sel.close()

if __name__ == "__main__":
    main()
