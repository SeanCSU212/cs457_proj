import socket

def main():
    host, port = "127.0.0.1", 12345
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            try:
                data = sock.recv(1024).decode()
                if not data:
                    break
                print(data, end="")
                if "your turn" in data.lower():
                    move = input("Enter your move (1-16): ")
                    sock.sendall(move.encode())
            except KeyboardInterrupt:
                print("Exiting game.")
                break

if __name__ == "__main__":
    main()
