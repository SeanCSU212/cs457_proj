import socket
import json

# Client configuration
host = '127.0.0.1'
port = 12358

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.sendall(message.encode())

def receive_response(sock):
    try:
        data = sock.recv(1024)
        if data:
            message = json.loads(data.decode())
            process_message(message)
        else:
            print("Server closed the connection")
            return False
    except (ConnectionResetError, json.JSONDecodeError):
        print("Error receiving or parsing server response")
        return False
    return True

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
    print(f"Chat from {data['sender']}: {data['message']}")

def handle_quit_broadcast(data):
    print(f"Player {data['player']} has quit the game.")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        
        while True:
            command = input("\nEnter command (join/chat/quit): ").strip()
            if command == "join":
                username = input("\nEnter your username: ").strip()
                send_message(sock, "join", {"username": username})
            elif command == "chat":
                message = input("\nEnter message: ").strip()
                send_message(sock, "chat", {"message": message})
            elif command == "quit":
                send_message(sock, "quit", {})
                break

            # Wait for and handle server response synchronously
            if not receive_response(sock):
                break

if __name__ == "__main__":
    main()