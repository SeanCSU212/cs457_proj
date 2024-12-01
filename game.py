game_board = [' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15','16']

win_conditions = [
        #Rows
        (0, 1, 2), (1, 2, 3), (4, 5, 6), (5, 6, 7),
        (8, 9, 10), (9, 10, 11), (12, 13, 14), (13, 14, 15),
        #Columns
        (0, 4, 8), (4, 8, 12), (1, 5, 9), (5, 9, 13),
        (2, 6, 10), (6, 10, 14), (3, 7, 11), (7, 11, 15),
        #Diagonals
        (0, 5, 10), (5, 10, 15), (3, 6, 9), (6, 9, 12),
        (1, 6, 11), (4, 9, 14), (2, 5, 8), (7, 10, 13)
]

def display_board():
    return (
        f"╔═══════════════════════════════════╗\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board[0]}   ║   {game_board[1]}   ║   {game_board[2]}   ║   {game_board[3]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board[4]}   ║   {game_board[5]}   ║   {game_board[6]}   ║   {game_board[7]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board[8]}   ║   {game_board[9]}   ║   {game_board[10]}   ║   {game_board[11]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board[12]}   ║   {game_board[13]}   ║   {game_board[14]}   ║   {game_board[15]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╚═══════════════════════════════════╝\n"
    )


def check_move_legality(input_num):
    input_index = input_num - 1
    if 0 <= input_index < 16 and game_board[input_index] not in {' X', ' O', ' +'}:
        return True
    return False
    
    
def make_move(input_num, player):
        game_board[input_num - 1] = player
        
def check_win():
    for move_set in win_conditions:
        x, y, z = move_set
        if game_board[x] == game_board[y] == game_board[z] != ' ':
            return True
    return False

def check_draw():
    if check_win() is None and all(position != ' ' for position in game_board):
        return True
    return False

def is_over():
    if check_draw() or check_win():
        return True
    else:
        return False

