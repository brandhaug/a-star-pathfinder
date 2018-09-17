import unittest
import a_star
from CellType import CellType


class TestAStar(unittest.TestCase):

    # Board-test.txt
    # '.', '.', '.', 'A', '.'
    # '.', '.', '.', '#', '.'
    # 'B', '.', '.', '.', '.'

    def test_load_board(self):
        board, initial_state, goal_state = a_star.load_board('board-test-1.txt')

        self.assertEqual(len(board), 3)
        self.assertEqual(len(board[0]), 5)
        self.assertEqual(board[1][2].x, 2)
        self.assertEqual(board[1][2].y, 1)
        self.assertEqual(board[1][2].type, '.')
        self.assertEqual(initial_state, (3, 0))
        self.assertEqual(goal_state, (0, 2))

    def test_initialize_board(self):
        board, initial_state, goal_state = a_star.load_board('board-test-1.txt')
        board = a_star.initialize_board(board, goal_state)

        # ================ NEIGHBORS ================ #

        # Top left cell - North neighbor does not exist

        # Top left cell - East neighbor
        self.assertEqual(board[0][0].neighbors[0].x, 1)
        self.assertEqual(board[0][0].neighbors[0].y, 0)

        #  Top left cell - South neighbor
        self.assertEqual(board[0][0].neighbors[1].x, 0)
        self.assertEqual(board[0][0].neighbors[1].y, 1)

        # Top left cell - West neighbor does not exist

        # Center cell - North neighbor
        self.assertEqual(board[1][2].neighbors[0].x, 2)
        self.assertEqual(board[1][2].neighbors[0].y, 0)

        # Center cell - East neighbor is an obstacle

        # Center cell - South neighbor
        self.assertEqual(board[1][2].neighbors[1].x, 2)
        self.assertEqual(board[1][2].neighbors[1].y, 2)

        # Center cell - West neighbor
        self.assertEqual(board[1][2].neighbors[2].x, 1)
        self.assertEqual(board[1][2].neighbors[2].y, 1)

        # Bottom right cell - North neighbor
        self.assertEqual(board[2][4].neighbors[0].x, 4)
        self.assertEqual(board[2][4].neighbors[0].y, 1)

        # Bottom right cell - East neighbor does not exist

        # Bottom right cell - South neighbor does not exist

        # Bottom right cell - West neighbor
        self.assertEqual(board[2][4].neighbors[1].x, 3)
        self.assertEqual(board[2][4].neighbors[1].y, 2)

        # ================ HEURISTIC FUNCTIONS ================ #
        self.assertEqual(board[1][0].h, 1)
        # self.assertEqual(round(board[1][1].h), 1.41) # Euclidean distance
        self.assertEqual(round(board[1][1].h), 2) # Manhattan distance



if __name__ == '__main__':
    unittest.main()
