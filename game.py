
game_board_numbers = [' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15','16']
game_board = ['  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ']

win_conditions = [
    # Rows
    (0, 1, 2), (1, 2, 3), 
    (4, 5, 6), (5, 6, 7), 
    (8, 9, 10), (9, 10, 11), 
    (12, 13, 14), (13, 14, 15),
    
    # Columns
    (0, 4, 8), (4, 8, 12), 
    (1, 5, 9), (5, 9, 13), 
    (2, 6, 10), (6, 10, 14), 
    (3, 7, 11), (7, 11, 15),
    
    # Diagonals (left to right)
    (0, 5, 10), (5, 10, 15), (1, 6, 11), (4, 9, 14), 

    # Diagonals (right to left)
    (3, 6, 9), (7, 10, 13), (6, 9, 12), (2, 5, 8)

]


def display_board():
    global game_board

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
def display_board_numbers():
    return (
        f"╔═══════════════════════════════════╗\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board_numbers[0]}   ║   {game_board_numbers[1]}   ║   {game_board_numbers[2]}   ║   {game_board_numbers[3]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board_numbers[4]}   ║   {game_board_numbers[5]}   ║   {game_board_numbers[6]}   ║   {game_board_numbers[7]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board_numbers[8]}   ║   {game_board_numbers[9]}   ║   {game_board_numbers[10]}   ║   {game_board_numbers[11]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╠ ═══════╬════════╬════════╬═══════ ╣\n"
        f"║        ║        ║        ║        ║\n"
        f"║   {game_board_numbers[12]}   ║   {game_board_numbers[13]}   ║   {game_board_numbers[14]}   ║   {game_board_numbers[15]}   ║\n"
        f"║        ║        ║        ║        ║\n"
        f"╚═══════════════════════════════════╝\n"
    )

def check_move_legality(input_num):
    if input_num == None:
        return False
    input_index = input_num - 1
    if 0 <= input_index < 16 and game_board[input_index] not in {' X', ' O', ' +'}:
        return True
    return False
    
def make_move(input_num, player):
        global game_board
        global game_board_numbers
        game_board[input_num - 1] = player
        game_board_numbers[input_num - 1] = player

        
def check_win():
    for move_set in win_conditions:
        x, y, z = move_set
        if game_board[x].strip() == game_board[y].strip() == game_board[z].strip() != '':
            return True
    return False

def check_draw():
    if not check_win() and all(position.strip() != '' for position in return_game_board()):
        return True
    else:
        return False

def is_over():
    if check_draw() or check_win():
        return True
    else:
        return False

def return_game_board():
    global game_board
    return game_board

def reset_game_board():
    global game_board
    global game_board_numbers
    game_board_numbers = [' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15','16']
    game_board = ['  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ','  ']