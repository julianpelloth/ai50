import unittest

from tictactoe import initial_state, player, actions, result, winner, terminal, utility

class MyTestCase(unittest.TestCase):

    def test_player(self):
        X = "X"
        O = "O"
        EMPTY = None

        self.assertEqual(player(initial_state()), X)

        board = [[EMPTY, X, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
        self.assertEqual(player(board), O)

        board = [[EMPTY, X, X],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(player(board), X)

        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        self.assertEqual(player(board), None)

    def test_actions(self):
        X = "X"
        O = "O"
        EMPTY = None

        self.assertEqual(actions(initial_state()),
                         [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])

        board = [[EMPTY, X, X],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(actions(board),
                         [(0, 0), (1, 1), (1, 2), (2, 0), (2, 1)])

        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        self.assertEqual(actions(board), None)

    def test_result(self):
        X = "X"
        O = "O"
        EMPTY = None

        self.assertEqual(result(initial_state(), (1, 1)),
                         [[EMPTY, EMPTY, EMPTY],
                          [EMPTY, X, EMPTY],
                          [EMPTY, EMPTY, EMPTY]])

        board = [[EMPTY, X, X],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(result(board, (1, 2)),
                         [[EMPTY, X, X],
                          [O, EMPTY, X],
                          [EMPTY, EMPTY, O]])

        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        try:
            result(board, (1, 1))
        except NameError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_winner(self):
        X = "X"
        O = "O"
        EMPTY = None

        self.assertEqual(winner(initial_state()), None)

        board = [[EMPTY, X, X],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertEqual(winner(board), None)

        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        self.assertEqual(winner(board), None)

        board = [[X, O, X],
                 [X, O, O],
                 [X, X, O]]
        self.assertEqual(winner(board), X)
        board = [[O, O, X],
                 [X, O, EMPTY],
                 [X, X, O]]
        self.assertEqual(winner(board), O)
        board = [[O, O, O],
                 [X, X, EMPTY],
                 [X, X, O]]
        self.assertEqual(winner(board), O)

    def test_terminal(self):
        X = "X"
        O = "O"
        EMPTY = None

        self.assertFalse(terminal(initial_state()))

        board = [[EMPTY, X, X],
                 [O, EMPTY, EMPTY],
                 [EMPTY, EMPTY, O]]
        self.assertFalse(terminal(board))

        board = [[X, O, X],
                 [X, O, O],
                 [O, X, X]]
        self.assertTrue(terminal(board))

        board = [[X, X, X],
                 [O, O, X],
                 [X, O, O]]
        self.assertTrue(terminal(board))
        board = [[O, EMPTY, X],
                 [EMPTY, O, EMPTY],
                 [X, X, O]]
        self.assertTrue(terminal(board))

    def test_utility(self):
        X = "X"
        O = "O"
        EMPTY = None

        board = [[X, O, X],
                 [X, X, O],
                 [O, X, O]]
        self.assertEqual(utility(board), 0)
        board = [[X, X, X],
                 [X, O, O],
                 [O, X, O]]
        self.assertEqual(utility(board), 1)
        board = [[X, O, O],
                 [X, O, EMPTY],
                 [O, X, X]]
        self.assertEqual(utility(board), -1)


if __name__ == '__main__':
    unittest.main()
