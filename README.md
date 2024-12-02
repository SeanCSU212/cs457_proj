# Tic-Tac-Toe-Two

**The 3-player, terminal based, Tic-Tac-Toe game...**

_by Jared Traub, Sean Cobb, and Seth Harling_

## About

Tic-Tac-Toe-Two is a terminal based game built within python. The game was created for the final project in CS 457: Computer Networks and the Internet at Colorado State University. The main purpose of the project is to develop a simple, multiplayer game demonstrating basic client-server architecture, and the fundamentals of socket programming.

## How to Run Game

1.  **Start the server:** Run the `server.py` script. USAGE: _python3 server.py -p [port]_

2.  **Connect clients:** Run the `client.py` script on **three** different client machines or terminals. USAGE: _python3 client.py -i [Server IP] -p [port]_

3.  **Enter Username:** Enter a custom username to join the game, once **three** players have joined and entered in their username, the game will automatically start.

4.  **Play the game:** Players take turns entering their moves when prompted. The first player to get three in a row (vertically, horizontally, or diagonally) wins!

## Game Message Protocol

Tic-Tac-Toe-Two was developed to use a standard JSON message protocol for all communications between the server and client.
*Server-to-Client Message Types*
- 'join_broadcast' - Sends message that a player has joined.
- 'start_game' - Sends message once 3 players have joined that the game is starting.
- 'display_board' - Sends message containing current formatted game board.
- 'display_board_numbers' - Sends message containing current formatted game board, with numbered positions. Meant to make playing move more intuitive when turn is prompted.
- 'your_turn' - Sends message prompting player for move input.
- 'wait_for_turn' - Sends message of current player making move to players who are not actively making move.
- 'move_broadcast' - Sends message of players move updating game state for all players.
- 'invalid_move' - Sends message when move input is invalid.
- 'game_over_win' - Sends message containing Winner of game.
- 'game_over_draw' - Sends message that game is over with no winner.
- 'play_again' - Sends message asking player if they would like to play again, or quit the program.
- 'quit_broadcast'- Sends message when player quits game.

*Client-to-Server Message Types
- 'join' - Activated upon client connection, Follows up by prompting user for Username, and assigns a playing piece (X,O,+). Allows up to 3 player to activly play, and remaining clients to join as spectators. Sends broadcast that new player joined to server and all connected clients.
- 'make_move' - Receives move position from client via "your_turn" message, handles all game logic following move including game state update, win conditions handling, and turn handling.

*'Quit' from client now handled exclusively through client disconnection handling in server.*

## Security

In terms of security, we have accounted for encryption but not authentication:

- Authentication - Users enter the game without using any sort of passphrase or key. This can lead to unwanted users joining the game. To address this, we could implement
  a password, giving authorized users the correct password to join the game. We could also create a user registration system where users could sign up for an account and their account can be validated by the server.

- Confidentiality - In our game we've implemented an encrypted connection using SSL encryption. We've created a private key and certificate for our server and included the files in our library. We made the certificate a value within the client so that they could verify the certificate. We then wrapped our the socket our server operates on with a secure socket to ensure an encrypted and confidential connection, we did the same with our client. This encrypts all users connections, protecting thier IP address from man-in-the-middle attacks.

## Technologies used

- Python
- Sockets

## Additional resources

- For more information and strategies on playing the game visit this link: [3 Player Tic-Tac-Toe](https://tictactoefree.com/tips/3-player-tic-tac-toe)

- [Python Documentation](https://docs.python.org/3/)

