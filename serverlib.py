import socket
import selectors
import types
import json
import game
import server
from server import players

def handle_message(sock, data, message):
    try:
        # Parse the incoming message
        msg = json.loads(message)
        msg_type = msg["type"]

        # Handling for players joining game
        if msg_type == "join":
            join_deserial(sock, data, msg["data"])
            if data not in server.players:
                server.players.append(data)
                if len(server.players) == 3:
                    server.start_game()
            return
        elif msg_type == "make_move":
            move_deserial(sock, data, msg["data"])
            return


        else:
            print(f"Unknown message type received: {msg_type}")
            return
        
    
    except json.JSONDecodeError:
        print("Received invalid JSON message")
    except KeyError as e:
        print(f"Missing expected key in message: {e}")



def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username
    data.sock = sock
    pieces = ["X", "O", "+"]
    if len(server.players) <= 3:
        data.piece = pieces[len(server.players)]
    else:
        data.peice = "Spectator"

    print(f"{username} joined the game with piece {data.piece} ")
    server.broadcast("join_broadcast", {"username": username})

# Handles moves made by player and game logic

def move_deserial(sock, data, msg_data):
    global players

    move = int(msg_data["move"]) # Integer of position input by active client

    if game.check_move_legality(move): # Check legality of move, if not legal, promp player again
        game.make_move(move, ' X' if server.turn_index == 0 else ' O' if server.turn_index == 1 else ' +') # Make move
        server.broadcast("move_broadcast", {"player": server.players[server.turn_index].username, "move": move}) # Broadcast move to all players
        server.broadcast("display_board", {"board": server.display_board()})
        print(game.display_board())
        
        if game.is_over():
            if game.check_win():
                server.broadcast("game_over_win", {"winner": server.players[server.turn_index].username})
            else:
                server.broadcast("game_over_draw", None)

            game.reset_game_board()

            print(game.display_board())
            server.broadcast("play_again", None)
            players.clear()



        else:
            server.turn_index = (server.turn_index + 1) % 3
            
            for x in range(3):
                if x == server.turn_index:
                    server.send_message(server.players[x].sock, "display_board_numbers", {"board": server.display_board_numbers()})
                    server.send_message(server.players[x].sock, "your_turn", None)

                else:
                    server.send_message(server.players[x].sock, "wait_for_turn", {"player": server.players[server.turn_index].username})
                
            
            
    else:   # Prompt player to resubmit move
        server.send_message(server.players[server.turn_index].sock, "invalid_move", {"move": move})
        server.send_message(server.players[server.turn_index].sock, "your_turn", None)
        