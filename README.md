#  _____ _         _____             _____              _____               
# |_   _(_) ___   |_   _|_ _  ___   |_   _|__   ___    |_   _|_      _____  
#   | | | |/ __|____| |/ _` |/ __|____| |/ _ \ / _ \_____| | \ \ /\ / / _ \ 
#   | | | | (_|_____| | (_| | (_|_____| | (_) |  __/_____| |  \ V  V / (_) |
#   |_| |_|\___|    |_|\__,_|\___|    |_|\___/ \___|     |_|   \_/\_/ \___/ 
                                                                           
This is a 3 player Tic-Tac-Toe game implemented using Python and sockets. It involves a 4x4 grid to play. Player one is X, player two is O, and player 3 is +.

## How to play
1. **Start the server:** Run the `server.py` script. USAGE: python3 server.py -p <port>.
2. **Connect clients:** Run the `client.py` script on three different machines or terminals. python3 client.py -i <Server IP> -p <port>
3. **Enter Username:** Enter username to join game, first 3 players to join will be active players.
3. **Play the game:** Players take turns entering their moves when prompted. The first player to get three in a row wins!

## Game Message Protocol
* 'join' - Activated upon client connection, Follows up by prompting user for Username, and assigns a playing piece (X,O,+). Allows up to 3 player to activly play, and remaining clients to join as spectators. Sends broadcast that new player joined to server and all connected clients.
* 'chat' - Activated by user, Follows up by promting user for message, broadcasts message back to server and to all connected clients.
* 'quit' - Activated by user Allows client to disconnect, sends broadcast to server and all connected clients.
* 'move' - Activated internally, prompts player to enter number of position (1-16), checks if valid move, and makes move for player.
* 'activate_turn' - Sent from server to client, toggles 'active_turn' variable in client


## Technologies used
* Python
* Sockets

## Additional resources
* For more information and strategies on playing the game visit this link: [3 Player Tic-Tac-Toe](https://tictactoefree.com/tips/3-player-tic-tac-toe)
* [Python Documentation](https://docs.python.org/3/)
* [Sockets Tutorial]

## Updates
* 11/16 - Join command updated to activate upon connection
* 11/16 - Game class updated for integration into server
* 11/16 - run_game() updated in serverlib
* 11/16 - Chat command updated to no longer prompt user for username
* 11/16 - Client updated to have 'active_turn' boolean for turn handling



