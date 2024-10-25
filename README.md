# 3-Player-Tic-Tac-Toe Game
This is a 3 player Tic-Tac-Toe game implemented using Python and sockets. It involves a 4x4 grid to play. Player one is X, player two is O, and player 3 is +.

## How to play
1. **Start the server:** Run the `server.py` script.
2. **Connect clients:** Run the `client.py` script on three different machines or terminals.
3. **Play the game:** Players take turns entering their moves. The first player to get three in a row wins!

## Game Message Protocol
* 'join' - Follows up by prompting user for Username, and assigns a playing piece (X,O,+). Command to join game, allows up to 3 player to activly play, and remaining clients to join as spectators. Sends broadcast that new player joined to server and all connected clients.
* 'chat' - Follows up by promting user for message, broadcasts message back to server and to all connected clients.
* 'quit' - Allows client to disconnect, sends broadcast to server and all connected clients.
* 'move' - Follows up by prompting user for coordinate to play (ex: 'A3'). The server then validates that no one has already played in that move, and if it is a valid move, places piece on game board. Server then handles game logic based on this move request.


## Technologies used
* Python
* Sockets

## Additional resources
* For more information and strategies on playing the game visit this link: [3 Player Tic-Tac-Toe](https://tictactoefree.com/tips/3-player-tic-tac-toe)
* [Python Documentation](https://docs.python.org/3/)
* [Sockets Tutorial]

