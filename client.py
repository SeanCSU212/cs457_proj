import socket
import json
import threading

host = '127.0.0.1'
port = 12358

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.sendall(message.encode())

def handle_server_response(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                message = json.loads(data.decode())
                process_message(message)
            else:
                print("Server closed the connection")
                break
        except (ConnectionResetError, json.JSONDecodeError):
            print("Error receiving or parsing server response")
            break

def process_message(message):
    msg_type = message["type"]
    if msg_type == "join_broadcast":
        handle_join_broadcast(message["data"])
    elif msg_type == "chat_broadcast":
        handle_chat_broadcast(message["data"])
    elif msg_type == "quit_broadcast":
        handle_quit_broadcast(message["data"])

def handle_join_broadcast(data):
    print(f"Player {data['username']} with piece {data['player']} has joined the game.")

def handle_chat_broadcast(data):
    print(f"Chat from {data['sender_id']}: {data['message']}")

def handle_quit_broadcast(data):
    print(f"Player {data['player']} has quit the game.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        threading.Thread(target=handle_server_response, args=(sock,)).start()
        
        while True:
            command = input("Enter command (join/chat/quit): ").strip()
            if command == "join":
                username = input("Enter your username: ").strip()
                send_message(sock, "join", {"username": username})
            elif command == "chat":
                message = input("Enter chat message: ").strip()
                send_message(sock, "chat", {"message": message})
            elif command == "quit":
                send_message(sock, "quit", {})
                break

if __name__ == "__main__":
    main()
