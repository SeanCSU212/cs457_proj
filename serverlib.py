import socket
import selectors
import types
import json

import game

sel = selectors.DefaultSelector()
clients = {}
CONNECTION_TIMEOUT = 60.0
connected_players = []



def check_and_start_game():
    if len(connected_players) == 3:
        print("3 Players Joined... Starting Game!")
        
        start_message = json.dumps({"type": "start", "data": "Game is starting!"}).encode('utf-8')
        for player_data in connected_players:
            player_data.outb += start_message
        broadcast_message("start_broadcast", None)
        run_game()


def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username
    clients[sock] = data
    players = ['X', 'O', '+']
    
    if (len(clients) > 3):
        print("Sorry, 3 players already joined! Stay connected to spectate and/or chat")
        data.player = "Spectator"

    else:
        data.player = players[len(clients) - 1] 

    print(f"{username} joined the game with piece {data.player} ")
    broadcast_message("join_broadcast", {"username": username, "player": data.player})

def chat_deserial(sock, data, msg_data):
    message = msg_data["message"]
    sender_id = data.username
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

def send_message(sock, msg_type, msg_data):
    message = json.dumps({"type": msg_type, "data": msg_data})
    sock.send(message.encode())

#Game working methods
def run_game():
    # Broadcast initial game board to all clients 
    print(game.display_board())
    broadcast_message("gameboard_broadcast", {"game_board": game.display_board()})
    
    for client_socket, player_data in clients.items():
        if player_data.player == "X":
            send_message(client_socket, "activate_turn", None)
            print("It's player X's turn!")
            break
    






'''
def run_game(player1, player2, player3):
    #Game setup
    cur_game = game(player1, player2, player3)
    game_over = False
    cur_player = cur_game.order[0]

    broadcast_message("start_message", "Welcome to 3 player tic-tac-toe, the game is turn based, you will enter the number of the space you want to put your mark in.")
    broadcast_message("ex_board", cur_game.example_board())
    
    while not game_over:
        broadcast_message("display_board", cur_game.display_board())
        broadcast_message("turn_notification", f"It's {cur_player.username}'s turn")
        
        # Place the other two players in a wait state
        for player in cur_game.wait:
            send_message(player.sock, "wait_state", "Please wait for your turn.")
        
        # TODO Accept move from player 1, verify, place on board
       
        #Check for win or tie
        if cur_game.check_win():
            broadcast_message("game_over", f"{cur_player.username} wins!")
            game_over = True
        elif cur_game.check_draw():
            broadcast_message("game_over", "It's a draw!")
            game_over = True
        else:
            # Switch to the next player and update wait state
            cur_game.next_turn()
            cur_player = cur_game.turn
'''
