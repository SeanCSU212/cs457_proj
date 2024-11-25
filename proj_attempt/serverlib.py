import socket
import selectors
import types
import json
import game
import server

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


        else:
            print(f"Unknown message type received: {msg_type}")

    except json.JSONDecodeError:
        print("Received invalid JSON message")
    except KeyError as e:
        print(f"Missing expected key in message: {e}")



def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username

    server.player_data[sock] = data
    pieces = ['X', 'O', '+']
    data.piece = pieces[len(server.players)]

    print(f"{username} joined the game with piece {data.piece} ")
    server.broadcast("join_broadcast", {"username": username})