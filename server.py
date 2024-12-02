import socket
import selectors
import types
import argparse
import json
import serverlib
import logging
import ssl
from game import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

sel = selectors.DefaultSelector()
players = []
turn_index = 0

''' Code for accepting client connections'''

def accept_wrapper(sock):
    try:
        conn, addr = sock.accept()
        logging.info(f"Accepted connection from {addr}")
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, data=types.SimpleNamespace(addr=addr))

    except socket.timeout:
        logging.warning(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")  # type: ignore
    except socket.error as e:
        logging.error(f"Socket error: {e}")

''' Code for handling connections and messages from clients'''

def service_connection(key, mask):
    global turn_index
    sock = key.fileobj
    data = key.data 

    if mask & selectors.EVENT_READ:
        try:
            message = sock.recv(1024).decode('utf-8').strip()
            if message:
                try:
                    serverlib.handle_message(sock, data, message)
                except socket.error as e:
                    logging.error(f"Socket error while receiving communication: {e}")
            else:
                # Handle client disconnection
                logging.info(f"Client {data.addr} disconnected.")
                serverlib.handle_client_disconnection(sock)
                sel.unregister(sock)
        except ConnectionResetError:
            # Handle abrupt disconnection
            logging.warning(f"Client {data.addr} abruptly disconnected.")
            serverlib.handle_client_disconnection(sock)
            sel.unregister(sock)


''' Code for sending messages to clients. '''

# Broadcast sends message to 
def broadcast(msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data}) + "\0"
    for client_socket in players:
        client_socket.sock.sendall(message.encode())

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data}) + "\0"
    sock.sendall(message.encode())

def main():
    # Handling for Arguments
    parser = argparse.ArgumentParser(description="Welcome to the Tic-Tac-Toe-Two Server! \nUSAGE: python3 server.py -p <port>")
    parser.add_argument('-p', '--port', type=str, required=True, help='Port Number')
    args = parser.parse_args()
    host = '0.0.0.0'  # Set static listening IP
    port = int(args.port)

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Encrypting connection and wrapping socket
    sec_con = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    sec_con.load_cert_chain(certfile="./secure/cert.pem", keyfile="./secure/key.pem")
    server_sock = sec_con.wrap_socket(server_sock, server_side=True)
    
    server_sock.bind((host, port))
    server_sock.listen()
    server_sock.setblocking(False)
    sel.register(server_sock, selectors.EVENT_READ, data=None)

    logging.info(f"Server running on {host}:{port}")

    try:
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    accept_wrapper(key.fileobj)
                else:
                    service_connection(key, mask)
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        sel.close()

if __name__ == "__main__":
    main()

