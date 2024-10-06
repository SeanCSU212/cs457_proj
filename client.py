import socket
import sys

def start_client(server_ip='0.0.0.0', server_port=12358):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")
        except ConnectionRefusedError:
            print("Error: connection refused")
            sys.exit(1)

        try:
            while True:
                message = input("Enter message to send: ")
                if message.lower() == 'exit':
                    break
                sock.sendall(message.encode('utf-8'))
                data = sock.recv(1024)
                print(f"Received from server: {data.decode('utf-8')}")

        except KeyboardInterrupt:
            print("Client is disconnecting...")
        except socket.error as e:
            print(f"Socket error: {e}")
        finally:
            print("Client disconnected")

if __name__ == "__main__":
    start_client()
