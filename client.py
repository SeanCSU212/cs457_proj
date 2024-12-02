import socket
import argparse
import json
import clientlib
import ssl

username = ""
sock = None

''' Code for sending message to server '''

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.sendall(message.encode()) 

def main():
    global username
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
    
    con_sec = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    con_sec.load_verify_locations('./secure/cert.pem')
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        #Wrap socket
        with con_sec.wrap_socket(sock, server_hostname=host) as ssock:
            
            try:
                ssock.connect((host, port))
                print(f"Connected to server at {host}:{port}")

                
                # Send the join message
                username = input("\nEnter Username: ")
                send_message(ssock, "join", {"username": username})

                # Buffer to handle partial and concatenated messages
                buffer = ""
                
                while True:
                    try:
                        # Receive data
                        data = ssock.recv(1024).decode("utf-8")
                        if not data:
                            print("Disconnected from server.")
                            break
                        
                        # Append data to the buffer
                        buffer += data

                        # Split messages by the delimiter '\0' and process them
                        messages = buffer.split("\0")
                        buffer = messages.pop()  # Keep the last incomplete message in the buffer

                        # Handle all complete messages
                        for message in messages:
                            if message.strip():  # Ignore empty messages
                                clientlib.handle_message(ssock, message)
                    
                    except KeyboardInterrupt:

                        print("Exiting game.")
                        break
                    except Exception as e:
                        print(f"Error during communication: {e}")
                        break

            except ConnectionRefusedError:
                print("Failed to connect to the server.")
            except Exception as e:
                print(f"Unexpected error: {e}")
            finally: 
                ssock.close() 
                sock.close()

if __name__ == "__main__":
    main()
