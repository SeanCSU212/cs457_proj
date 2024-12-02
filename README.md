# Tic-Tac-Toe-Two

**The 3-player, terminal based, Tic-Tac-Toe game...**

_by Jared Traub, Sean Cobb, and Seth Harling_

## About

Tic-Tac-Toe-Two is a terminal based game built within python. The game was created for the final project in CS 457: Computer Networks and the Internet at Colorado State University. The main purpose of the project is to develop a simple, multiplayer game demonstrating basic client-server architecture, and the fundamentals of socket programming.

## How to play

1.  **Start the server:** Run the `server.py` script. USAGE: _python3 server.py -p [port]_

2.  **Connect clients:** Run the `client.py` script on **three** different machines or terminals. USAGE: _python3 client.py -i [Server IP] -p [port]_

3.  **Enter Username:** Enter a custom username to join the game, once **three** players have joined, the game will automatically start.

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

- 'quit' - Activated by user Allows client to disconnect, sends broadcast to server and all connected clients.

- 'move' - Activated internally, prompts player to enter number of position (1-16), checks if valid move, and makes move for player.

## Security

In terms of security, our game lacks in two main ways:

- Authentication - Users enter the game without using any sort of passphrase or key. This can lead to unwanted users joining the game. To address this, we could implement
  a password or private key feature, giving authorized users the correct password or private key to join the game. We could also create a user registration system where users could sign up for an account and their account can be validated by the server.

- Confidentiality - The methods mentioned above, although important, would be useless without implementing an encryption system to keep our data from being sent over the internet in plaintext. To address this we can implement public/private key encryption within our game to have our data stay safe in transmission.

## Technologies used

- Python
- Sockets

## Additional resources

- For more information and strategies on playing the game visit this link: [3 Player Tic-Tac-Toe](https://tictactoefree.com/tips/3-player-tic-tac-toe)

- [Python Documentation](https://docs.python.org/3/)

## Updates

- 11/16 - Join command updated to activate upon connection

- 11/16 - Game class updated for integration into server

- 11/16 - run_game() updated in serverlib

- 11/16 - Chat command updated to no longer prompt user for username

- 11/16 - Client updated to have 'active_turn' boolean for turn handling
