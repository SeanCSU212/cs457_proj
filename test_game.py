import unittest
from game import *

class TestGameBoard(unittest.TestCase):
    def setUp(self):
        # Ensure the game board is reset before each test
        reset_game_board()

    def test_display_board(self):
        # Check if the initial board display matches expectations
        expected_board = (
            "╔═══════════════════════════════════╗\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "╠ ═══════╬════════╬════════╬═══════ ╣\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "╠ ═══════╬════════╬════════╬═══════ ╣\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "╠ ═══════╬════════╬════════╬═══════ ╣\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "║        ║        ║        ║        ║\n"
            "╚═══════════════════════════════════╝\n"
        )
        self.assertEqual(display_board(), expected_board)

    def test_check_move_legality(self):
        # Test legal moves
        self.assertTrue(check_move_legality(1))  # First cell
        self.assertTrue(check_move_legality(16))  # Last cell
        # Test illegal moves
        make_move(1, ' X')
        self.assertFalse(check_move_legality(1))  # Already occupied
        self.assertFalse(check_move_legality(17))  # Out of bounds
        self.assertFalse(check_move_legality(0))  # Out of bounds

    def test_make_move(self):
        make_move(1, ' X')
        self.assertEqual(return_game_board()[0], ' X')
        make_move(16, ' O')
        self.assertEqual(return_game_board()[15], ' O')

    def test_check_win(self):
        # Horizontal win
        make_move(1, ' X')
        make_move(2, ' X')
        make_move(3, ' X')
        self.assertTrue(check_win())
        reset_game_board()
        # Vertical win
        make_move(1, ' O')
        make_move(5, ' O')
        make_move(9, ' O')
        self.assertTrue(check_win())
        reset_game_board()
        # Diagonal win
        make_move(1, ' +')
        make_move(6, ' +')
        make_move(11, ' +')
        self.assertTrue(check_win())

    def test_check_draw(self):
        # Fill the board without any winning conditions
        moves = [
            (1, ' X'), (2, ' O'), (3, ' +'), (4, ' X'),
            (5, ' O'), (6, ' X'), (7, ' O'), (8, ' +'),
            (9, ' X'), (10, ' +'), (11, ' O'), (12, ' X'),
            (13, ' +'), (14, ' O'), (15, ' X'), (16, ' +')
        ]
        for move, player in moves:
            make_move(move, player)
            
        self.assertTrue(check_draw())
        self.assertFalse(check_win())

    def test_is_over(self):
        make_move(1, ' X')
        make_move(2, ' X')
        make_move(3, ' X')
        self.assertTrue(is_over())  # Game ends on a win
        reset_game_board()
        moves = [
            (1, ' X'), (2, ' O'), (3, ' +'), (4, ' X'),
            (5, ' O'), (6, ' X'), (7, ' O'), (8, ' +'),
            (9, ' X'), (10, ' +'), (11, ' O'), (12, ' X'),
            (13, ' +'), (14, ' O'), (15, ' X'), (16, ' +')
        ]
        for move, player in moves:
            make_move(move, player)
        self.assertTrue(is_over())  # Game ends on a draw

    def test_reset_game_board(self):
        make_move(1, ' X')
        reset_game_board()
        self.assertEqual(game_board, ['  '] * 16)
        self.assertEqual(game_board_numbers, [f'{i:2}' for i in range(1, 17)])

if __name__ == '__main__':
    unittest.main()
