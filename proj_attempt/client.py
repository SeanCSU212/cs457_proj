import socket
import argparse

def main():

    parser = argparse.ArgumentParser(
        description = "Welcome to the Tic-Tac-Toe-Two Client! \nUSAGE: python3 client.py -i <Server IP> -p <port>",
        epilog = "HOW TO PLAY: \n\n 1. Wait for 3 players to connect \n 2. Wait for your turn, the server will message you when it is your turn \n 3. Upon your turn, enter the MOVE command, followed by the 2 character letter-number combo of the space you want tot move to. \n(Players can only play on spaces that have not yet been played on) \n4. The first player to get 3 in a row (vertically, horizontally, or diagonally) Wins! \n\n GOOD LUCK!",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-i', '--serveraddress', type=str, required=True, help='Server IP Address')
    parser.add_argument('-p', '--port', type=str, required=True, help='Port Number')
    parser.add_argument('-n', '--dns', type=str, )
    args = parser.parse_args()


    host = args.serveraddress
    port = int(args.port)
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
