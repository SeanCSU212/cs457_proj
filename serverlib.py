import socket
import selectors
import types
import json

import game



clients = {}

CONNECTION_TIMEOUT = 60.0

game_board = [["","","",""],["","","",""],["","","",""],["","","",""]]

connected_players = []

def check_and_start_game():
    if len(connected_players) == 3:
        print("3 Players Joined... Starting Game!")
        
        start_message = json.dumps({"type": "start", "data": "Game is starting!"}).encode('utf-8')
        for player_data in connected_players:
            player_data.outb += start_message
        broadcast_message("start_broadcast", None)
        playerX  = connected_players[0]
        playerO = connected_players[1]
        playerPlus = connected_players[2]
        run_game(playerX, playerO, playerPlus)

        


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

def run_game(player1, player2, player3):
    #Create instance of game object, passsing in player 1,2,3

    #Broadcast starting message to all clients
    #Broadcast empty game board to all clients
    #List for active player, list for waiting player, players can only use "move" command when in active list

    #While loop (while win condition has not been met)
        #Put player 1 in active list, player 2 and 3 in wait state
        #Accept move from player 1, verify, place on board
        #Check for win (breaks loop)
        #Broadcast updated board to to all clients
        #Incriment active player, move other to waitlist

    print(player1)
    print(player2)
    print(player3)

