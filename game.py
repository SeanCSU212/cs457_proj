import random
import player


'''
def __init__(self, player1, player2, player3):
    self.player1 = player1
    self.player2 = player2
    self.player3 = player3
    self.player_list = [player1, player2, player3]
    
    self.order = random.shuffle(self.player_list)
    self.turn = self.order[0]
    self.wait = [self.order[1], self.order[2]]
    
    self.game_board = [
        ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ',
        ' ', ' ', ' ', ' ']
    self.win_conditions = [
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
    '''

game_board = [' 1',' 2',' 3',' 4',' 5',' 6',' 7',' 8',' 9','10','11','12','13','14','15','16']

def display_board():
    return (
        f"{game_board[0]}|{game_board[1]}|{game_board[2]}|{game_board[3]}\n"
        f"--|--|--|--\n"
        f"{game_board[4]}|{game_board[5]}|{game_board[6]}|{game_board[7]}\n"
        f"--|--|--|--\n"
        f"{game_board[8]}|{game_board[9]}|{game_board[10]}|{game_board[11]}\n"
        f"--|--|--|--\n"
        f"{game_board[12]}|{game_board[13]}|{game_board[14]}|{game_board[15]}\n"
    )

def check_move_legality(self, board_num):
    if self.game_board[board_num - 1] in {'x', 'o', '+'}:
        return False
    elif board_num >= 1 and board_num <= 16:
        return False
    else:
        return True
    
    
def make_move(player, input_num):
    if(check_move_legality(input_num)):
        return
        
def check_win(self):
    for move_set in self.win_conditions:
        x, y, z = move_set
        
        if self.game_board[x] == self.game_board[y] == self.game_board[z] != ' ':
            return True
    return False

def check_draw(self):
    if self.check_win() is None and all(position != ' ' for position in self.game_board):
        return True
    return False
