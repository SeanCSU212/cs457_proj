import socket
import selectors
import types
import json
import game
import server
import logging
from server import players, sel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


''' Code for accepting, deserializing, and handling JSON messages from client '''

def handle_message(sock, data, message):
    try:
        # Parse the incoming message
        msg = json.loads(message)
        msg_type = msg["type"]

        if msg_type == "join":
            join_deserial(sock, data, msg["data"])
            if data not in server.players:
                server.players.append(data)
                if len(server.players) == 3:
                    start_game()
            return
        elif msg_type == "make_move":
            move_deserial(sock, data, msg["data"])
            return
        else:
            logging.warning(f"Unknown message type received: {msg_type}")
            return

    except json.JSONDecodeError:
        logging.error("Received invalid JSON message.")
    except KeyError as e:
        logging.error(f"Missing expected key in message: {e}")


''' Code for handling joining of players '''

def join_deserial(sock, data, msg_data):
    username = msg_data["username"]
    data.username = username
    data.sock = sock
    pieces = ["X", "O", "+"]
    if len(server.players) <= 3:
        data.piece = pieces[len(server.players)]
    else:
        data.piece = "Spectator"

    logging.info(f"{username} joined the game with piece {data.piece}.")
    server.broadcast("join_broadcast", {"username": username})


''' Code for handling intentional/unintentional disconnection of clients'''

def handle_client_disconnection(sock):
    disconnected_player = None
    for player in players:
        if player.sock == sock:
            disconnected_player = player
            players.remove(player)
            break

    if disconnected_player:
        server.broadcast("quit_broadcast", {"player": disconnected_player.username})
        logging.info(f"Player {disconnected_player.username} disconnected.")

        if len(players) == 2:  # Game was ongoing
            server.broadcast("game_over_draw", None)
            game.reset_game_board()
            server.broadcast("play_again", None)
            players.clear()
        sock.close()


''' Code for handling the start of game'''

def start_game():
    # Broadcast starting game message to all clients
    server.broadcast("start_game", {"board": server.display_board()})

    logging.info(f"Players: {players[server.turn_index]}")
    logging.info("\n3 Players joined, starting game\n")
    logging.info(server.display_board())

    # Send "your_turn" message to the current player's socket
    server.send_message(players[server.turn_index].sock, "display_board_numbers", {"board": server.display_board_numbers()})
    server.send_message(players[server.turn_index].sock, "your_turn", None)


''' Code for accepting moves from players, and handling all game logic '''

def move_deserial(sock, data, msg_data):
    global players
    if len(players) < 3:  # If game is inactive, return
        logging.warning("Move received, but the game is not active yet.")
        return

    if msg_data["move"] == "":
        server.send_message(server.players[server.turn_index].sock, "invalid_move", {"move": ""})
        server.send_message(server.players[server.turn_index].sock, "your_turn", None)
        return
    try:
        if "move" not in msg_data:
            raise ValueError("Missing 'move' key in the input data.")
        
        move = int(msg_data["move"])
        
       
        if not (1 <= move <= 16):  
            raise ValueError(f"'move' value {move} is out of range.") 
    except ValueError as e:
        print(f"Invalid input: {e}")
        move = None    
            
    if game.check_move_legality(move):  # Check legality of move
        game.make_move(move, ' X' if server.turn_index == 0 else ' O' if server.turn_index == 1 else ' +')
        logging.info(f"Player {server.players[server.turn_index].username} made a move at position {move}.")
        server.broadcast("move_broadcast", {"player": server.players[server.turn_index].username, "move": move})
        server.broadcast("display_board", {"board": server.display_board()})
        logging.info(game.display_board())

        if game.is_over():
            if game.check_win():
                server.broadcast("game_over_win", {"winner": server.players[server.turn_index].username})
                logging.info(f"Player {server.players[server.turn_index].username} won the game.")
            else:
                server.broadcast("game_over_draw", None)
                logging.info("Game ended in a draw.")

            game.reset_game_board()
            logging.info("Game board has been reset.")
            logging.info(game.display_board())
            server.broadcast("play_again", None)
            players.clear()

        else:
            server.turn_index = (server.turn_index + 1) % 3
            for x in range(3):
                if x == server.turn_index:
                    server.send_message(server.players[x].sock, "display_board_numbers", {"board": server.display_board_numbers()})
                    server.send_message(server.players[x].sock, "your_turn", None)
                    logging.info(f"It is now {server.players[x].username}'s turn.")
                else:
                    server.send_message(server.players[x].sock, "wait_for_turn", {"player": server.players[server.turn_index].username})
    else:  # Prompt player to resubmit move
        logging.warning(f"Illegal move attempted by player {server.players[server.turn_index].username} at position {move}.")
        server.send_message(server.players[server.turn_index].sock, "invalid_move", {"move": move})
        server.send_message(server.players[server.turn_index].sock, "your_turn", None)
