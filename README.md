# Tic-Tac-Toe-Two

**The 3-player, terminal based, Tic-Tac-Toe game...** 

*by Jared Traub, Sean Cobb, and Seth Harling*

## About
Tic-Tac-Toe-Two is a terminal based game built within python. The game was created for the final project in CS 457: Computer Networks and the Internet at Colorado State University. The main purpose of the project is to develop a simple, multiplayer game demonstrating basic client-server architecture, and the fundamentals of socket programming. 
	

## How to play

1.  **Start the server:** Run the `server.py` script. USAGE: *python3 server.py -p [port]*

2.  **Connect clients:** Run the `client.py` script on **three** different machines or terminals. USAGE: *python3 client.py -i [Server IP] -p [port]*

3.  **Enter Username:** Enter a custom username to join the game, once **three** players have joined, the game will automatically start.

3.  **Play the game:** Players take turns entering their moves when prompted. The first player to get three in a row (vertically, horizontally, or diagonally) wins!

## Game Message Protocol

Tic-Tac-Toe-Two was developed to use a standard JSON message protocol for all communications between the server and client. 

* 'join' - Activated upon client connection, Follows up by prompting user for Username, and assigns a playing piece (X,O,+). Allows up to 3 player to activly play, and remaining clients to join as spectators. Sends broadcast that new player joined to server and all connected clients.

* 'chat' - Activated by user, Follows up by prompting user for message, broadcasts message back to server and to all connected clients.

* 'quit' - Activated by user Allows client to disconnect, sends broadcast to server and all connected clients.

* 'move' - Activated internally, prompts player to enter number of position (1-16), checks if valid move, and makes move for player.

  
  

## Technologies used

* Python
* Sockets
  
## Additional resources

* For more information and strategies on playing the game visit this link: [3 Player Tic-Tac-Toe](https://tictactoefree.com/tips/3-player-tic-tac-toe)

*  [Python Documentation](https://docs.python.org/3/)
  

## Updates

* 11/16 - Join command updated to activate upon connection

* 11/16 - Game class updated for integration into server

* 11/16 - run_game() updated in serverlib

* 11/16 - Chat command updated to no longer prompt user for username

* 11/16 - Client updated to have 'active_turn' boolean for turn handling


