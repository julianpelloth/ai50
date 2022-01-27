import unittest

from minesweeper import *

# Simple tests just for debugging
class MyTestCase(unittest.TestCase):

    def test_safe_mines(self):
        ai = MinesweeperAI()
        ai.knowledge.append(Sentence({(0, 1), (1, 1), (1, 0)}, 0))

        ai.safe_mines()
        self.assertEqual(ai.safes, {(0, 1), (1, 1), (1, 0)})

    def test_add_knowledge(self):

        ai = MinesweeperAI()
        ai.add_knowledge((0, 0), 0)

        self.assertEqual(ai.safes, {(0, 1), (1, 1), (1, 0), (0, 0)})


if __name__ == '__main__':
    unittest.main()
