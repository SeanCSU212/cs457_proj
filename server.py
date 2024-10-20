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
        conn.settimeout(CONNECTION_TIMEOUT)  # Set timeout for client connection
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)

        clients[conn] = data

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
                print(f"Received message from {data.addr}: {message}")
                
                try:
                    json_message = json.loads(message)
                    deserialize(sock, json_message, data)
                except json.JSONDecodeError:
                    print("ERROR: Received invalid json")
            else:
                print(f"Closing connection to {data.addr}")
                sel.unregister(sock)
                sock.close()
                if sock in clients:
                    del clients[sock]  # Ensure client is removed on close
        except socket.timeout:
            print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
        except socket.error as e:
            print(f"SOCKET ERROR IN COMMUNICATION: {e}")

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            try:
                sent = sock.send(data.outb)
                print(f"Sent message to {data.addr}: {data.outb[:sent].decode('utf-8')}")
                data.outb = data.outb[sent:]
            except socket.timeout:
                print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
            except socket.error as e:
                print(f"SOCKET ERROR IN COMMUNICATION: {e}")

# For handling deserialized messages
def deserialize(sock, message, data):
    msg_type = message["type"]
    username = message["username"]
    
    if msg_type == "join":
        join_deserial(sock, message)

    elif msg_type == "chat":
        chat_deserial(sock, message)

    elif msg_type == "quit":
        quit_deserial(sock, message)

# Deserialize messages by type
def join_deserial(sock, message):
    username = message["username"]
    response = {
        "type": "join_ack",
        "username": message["username"],
        "data": {
            "message": f"Welcome to the game {username}!"
        }
    }
    sock.send(json.dumps(response).encode('utf-8'))

def chat_deserial(sock, data):
    message = data["message"]
    username = data["username"]

    print(f"Chat from {username}: {message}")
    
    broadcast_message("chat_broadcast", {"sender": username, "message": message})

def broadcast_message(msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    to_remove = []
    
    for client_socket in clients:
        try:
            client_socket.send(message.encode())
        except BrokenPipeError:
            print(f"Broken pipe for client {clients[client_socket].addr}, removing from list.")
            to_remove.append(client_socket)
    
    # Remove clients after broadcasting
    for client_socket in to_remove:
        del clients[client_socket]

def quit_deserial(sock, message):
    username = message["username"]
    print(f"{username} has quit the game.")
    sel.unregister(sock)
    sock.close()
    if sock in clients:
        del clients[sock]

host = '0.0.0.0'
port = 12359
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