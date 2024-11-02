import socket
import selectors
import types
import json
import argparse
import sys

import serverlib




sel = selectors.DefaultSelector()
parser = argparse.ArgumentParser(description = "Welcome to the Tic-Tac-Toe-Two Server! \nUSAGE: python3 server.py <Server IP> <port>")

parser.add_argument('-i', '--ipaddress', type=str, required=True, help='Host IP Address')
parser.add_argument('-p', '--port', type=str, required=True, help='Port Number')

args = parser.parse_args()


host = args.ipaddress
port = int(args.port)

def handle_message(sock, data, message):
    try:
        msg = json.loads(message)
        msg_type = msg["type"]
        if msg_type == "join":
            serverlib.join_deserial(sock, data, msg["data"])
            if data not in serverlib.connected_players:
                serverlib.connected_players.append(data)
                serverlib.check_and_start_game()
        elif msg_type == "chat":
            serverlib.chat_deserial(sock, data, msg["data"])
        elif msg_type == "quit":
            serverlib.quit_deserial(sock, data)
    except json.JSONDecodeError:
        print("Received invalid JSON message")

def accept_wrapper(sock):
    try:
        conn, addr = sock.accept()
        print(f"Accepted connection from {addr}")
        conn.setblocking(False)
        data = types.SimpleNamespace(addr=addr, inb=b"", outb=b"", player=None, username=None)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        sel.register(conn, events, data=data)
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
                handle_message(sock, data, message)
            else:
                print(f"Closing connection")
                sel.unregister(sock)
                sock.close()
        except socket.timeout:
            print(f"Connection timed out after {CONNECTION_TIMEOUT} seconds")
        except socket.error as e:
            print(f"Socket error while receiving communication: {e}")

    if mask & selectors.EVENT_WRITE:
        if data.outb:
            try:
                sent = sock.send(data.outb)
                data.outb = data.outb[sent:]
            except socket.error as e:
                print(f"Socket error while sending communication: {e}")





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





