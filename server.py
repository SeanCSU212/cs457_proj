import socket
import selectors
import types
import json

sel = selectors.DefaultSelector()

clients = {}

CONNECTION_TIMEOUT = 60.0

def accept_wrapper(sock):
    try:
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", player=None, username=None)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
    except socket.timeout:
        print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
    except socket.error as e:
        print(f"Socket error: {e}")

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data

    if mask & selectors.EVENT_READ:
        try:
            recv_data = sock.recv(1024)
            if recv_data:
                message = recv_data.decode('utf-8')
                handle_message(sock, data, message)
            else:
                print(f"Closing connection")
                sel.unregister(sock)
                sock.close()
        except socket.timeout:
            print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
        except socket.error as e:
            print(f"Socket error while receiving communication: {e}")

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            try:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
            except socket.error as e:
                print(f"Socket error while sending communication: {e}")

def handle_message(sock, data, message):
    try:
        msg = json.loads(message)
        msg_type = msg["type"]
        if msg_type == "join":
            join_deserial(sock, data, msg["data"])
        elif msg_type == "chat":
            chat_deserial(sock, data, msg["data"])
        elif msg_type == "quit":
            quit_deserial(sock, data)
    except json.JSONDecodeError:
        print("Received invalid JSON message")

def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username
    clients[sock] = data
    players = ['X', 'O', '+']
    data.player = players[len(clients) - 1] 
    
    if (len(clients) >= 3):
        print("Sorry, 3 players already joined! Stay connected to spectate and/or chat")

    print(f"{username} joined the game with piece {data.player} ")

    broadcast_message("join_broadcast", {"username": username, "player": data.player})

def chat_deserial(sock, data, msg_data):
    username = msg_data["username"]
    message = msg_data["message"]
    sender_id = data.player
    print(f"Chat message from {username} playing as {sender_id}: {message}")
    broadcast_message("chat_broadcast", {
        "sender_id": sender_id,
        "message": message
    })

def quit_deserial(sock, data):
    player_id = data.player_id
    broadcast_message("quit_broadcast", {"player_id": player_id})
    print(f"Player {player_id} quit the game")
    if sock in clients:
        del clients[sock]

def broadcast_message(msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    for client_socket in clients:
        client_socket.send(message.encode())


host = '0.0.0.0'
port = 12358

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
lsock.bind((host, port))
lsock.listen()
print(f"Listening on {host}:{port}")
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                service_connection(key, mask)
except KeyboardInterrupt:
    print("Server is shutting down")
finally:
    sel.close()
