import socket
import sys
import json

username = ''

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
                action_type = input("Enter action (quit): ")
                if action_type == 'quit':
                    send_quit(sock, username)
                    break
                data = sock.recv(1024)
                print(f"Received from server: {data.decode('utf-8')}")

        except KeyboardInterrupt:
            print("Client is disconnecting...")
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            print("Client disconnected")

#For sending json messages
def send_join(sock, username):
    message = {
        "type": "join",
        "username": username
    }
    sock.send(json.dumps(message).encode('utf-8'))

def send_quit(sock, username):
    message = {
        "type": "quit",
        "username": username
    }
    sock.send(json.dumps(message).encode('utf-8'))
    
if __name__ == "__main__":
    start_client()
