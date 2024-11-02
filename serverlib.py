import socket
import selectors
import types
import json



clients = {}

CONNECTION_TIMEOUT = 60.0

game_board = [["","","",""],["","","",""],["","","",""],["","","",""]]



def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username
    clients[sock] = data
    players = ['X', 'O', '+']
    data.player = players[len(clients) - 1] 
    
    if (len(clients) >= 3):
        print("Sorry, 3 players already joined! Stay connected to spectate and/or chat")

    print(f"{username} joined the game with piece {data.player} ")

    broadcast_message("join_broadcast", {"username": username, "player": data.player})

def chat_deserial(sock, data, msg_data):
    message = msg_data["message"]
    sender_id = data.player
    print(f"Chat message from {sender_id}: {message}")
    broadcast_message("chat_broadcast", {
        "sender_id": sender_id,
        "message": message
    })

def quit_deserial(sock, data):
    username = data.username
    broadcast_message("quit_broadcast", {"username": username})
    print(f"Player {username} quit the game")
    if sock in clients:
        del clients[sock]

def broadcast_message(msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    for client_socket in clients:
        client_socket.send(message.encode())
