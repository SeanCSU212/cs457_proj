import socket
import sys
import json

def start_client(server_ip='0.0.0.0', server_port=12359):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")
        except ConnectionRefusedError:
            print("Error: connection refused")
            sys.exit(1)

        username = input("Enter username: ")
        send_join(sock, username)

        try:
            while True:
                action_type = input("Enter action (chat/quit): ").strip().lower()

                if action_type == 'quit':
                    send_quit(sock, username)
                    break

                elif action_type == 'chat':
                    message = get_message()
                    send_chat(sock, username, message)
                
                data = sock.recv(1024)
                if not data:
                    print("Disconnected from server.")
                    break

                process_server_message(data.decode('utf-8'))

        except KeyboardInterrupt:
            print("Client is disconnecting...")
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            print("Client disconnected")


def send_join(sock, username):
    """Send a join request to the server."""
    message = {
        "type": "join",
        "username": username
    }
    sock.send(json.dumps(message).encode('utf-8'))


def send_chat(sock, username, message):
    """Send a chat message to the server."""
    message = {
        "type": "chat",
        "username": username,
        "message": message
    }
    sock.send(json.dumps(message).encode('utf-8'))


def send_quit(sock, username):
    """Send a quit request to the server."""
    message = {
        "type": "quit",
        "username": username
    }
    sock.send(json.dumps(message).encode('utf-8'))


def get_message():
    """Get chat message from user."""
    return input("Enter message: ")


def process_server_message(data):
    """Process messages received from the server."""
    try:
        json_data = json.loads(data)
        msg_type = json_data.get("type")

        if msg_type == "join_ack":
            print(f"Server: {json_data['data']['message']}")

        elif msg_type == "chat_broadcast":
            sender = json_data['data']['sender']
            message = json_data['data']['message']
            print(f"{sender}: {message}")

        else:
            print(f"Unknown message type: {msg_type}")

    except json.JSONDecodeError:
        print("Error: Received invalid JSON from server.")
    except KeyError:
        print("Error: Missing fields in server response.")


if __name__ == "__main__":
    start_client()