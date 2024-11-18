import socket
import selectors
import types
from game import *

sel = selectors.DefaultSelector()
players = []
turn_index = 0

def accept_wrapper(sock):
    conn, addr = sock.accept()
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, data=types.SimpleNamespace(addr=addr))
    players.append(conn)
    conn.sendall(f"Welcome player {len(players)}\n".encode())
    if len(players) == 3:
        start_game()

def start_game():
    for player in players:
        player.sendall("Game started! Here is the board:\n".encode())
        player.sendall(display_board().encode())
    players[turn_index].sendall("It's your turn!\n".encode())

def service_connection(key, mask):
    global turn_index
    sock = key.fileobj
    if mask & selectors.EVENT_READ:
        data = sock.recv(1024).decode().strip()
        if data:
            try:
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


def broadcast(message):
    for player in players:
        player.sendall(message.encode())

def main():
    host, port = "127.0.0.1", 12345
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
