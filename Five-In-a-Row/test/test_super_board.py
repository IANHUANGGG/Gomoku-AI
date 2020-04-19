import unittest
from src.super_board import SuperBoard
from src.direction import Direction as D
from operator import add, sub
from src.piece import Piece as P
from src.thread import ThreadType, ThreadLevel, Extense, Reward

class TestSuperBoard(unittest.TestCase):

    def setUp(self):
        self.sb_1 = SuperBoard()
        self.customized_board = [[P.WHITE, P.EMPTY, P.EMPTY, P.WHITE, P.WHITE, 
                            P.BLACK, P.BLACK, P.BLACK, P.EMPTY, P.EMPTY,
                            P.EMPTY, P.WHITE, P.WHITE, P.WHITE, P.WHITE]
                            ]
        self.sb_2 = SuperBoard(self.customized_board)
        self.customized_b2 = [[P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY],
                              [P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY, P.EMPTY]]

    def test_default_constructor(self):
        self.assertTrue(self.sb_1.board == [[P.EMPTY for col in range(15)] for row in range(15)] and
                        self.sb_1.height == 15 and self.sb_1.width == 15 and
                        self.sb_1.valued_moves == set((7,7)), self.sb_1.winner == None and 
                        self.sb_1.reward == 0 and self.sb_1.score == 0)
    
    def test_constructor_with_board(self):
        self.assertTrue(self.sb_2.board == self.customized_board and
                        self.sb_2.height == 1 and self.sb_2.width == 15 and
                        self.sb_2.valued_moves == set((7,7)), self.sb_2.winner == None and 
                        self.sb_2.reward == 0 and self.sb_2.score == 0)

    def test_consecutive_pieces(self):
        self.assertEqual(self.sb_2.consecutive_pieces(0, 8, D.RIGHT, sub), (P.BLACK, 3, False))
        self.assertEqual(self.sb_2.consecutive_pieces(0, 9, D.RIGHT, sub), (P.EMPTY, 0, True))
        self.assertEqual(self.sb_2.consecutive_pieces(0, 5, D.RIGHT, sub), (P.WHITE, 2, True))
        self.assertEqual(self.sb_2.consecutive_pieces(0, 1, D.RIGHT, sub), (P.WHITE, 1, False))
        self.assertEqual(self.sb_2.consecutive_pieces(0, 10, D.RIGHT, add), (P.WHITE, 4, False))

    def test_case_indiv(self):
        cp = (P.BLACK, 2, True)
        expected = [Reward(ThreadType(ThreadLevel.TWO, Extense.OPEN, False), True)]
        self.assertEqual(self.sb_1.case_indiv(P.BLACK, cp), expected)

    def test_case_indiv2(self):
        cp2 = (P.BLACK, 4, False)
        expected2 = [Reward(ThreadType(ThreadLevel.FOUR, Extense.HALF_OPEN, False), False)]
        self.assertEqual(self.sb_1.case_indiv(P.WHITE, cp2), expected2)

    def test_case_indiv3(self):
        cp3 = (P.BLACK, 3, False)
        expected3 = [Reward(ThreadType(ThreadLevel.THREE, Extense.CLOSED, False), False)]
        self.assertEqual(self.sb_1.case_indiv(P.WHITE, cp3, False), expected3)

    def test_case_indiv4(self):
        cp4 = (P.BLACK, 4, False)
        expected4 = [Reward(ThreadType(ThreadLevel.FOUR, Extense.HALF_OPEN, False), False)]
        self.assertEqual(self.sb_1.case_indiv(P.WHITE, cp4, False), expected4)
        
    def test_case_same_type(self):
        cp1 = (P.BLACK, 1, True)
        cp2 = (P.BLACK, 1, True)
        expected = [Reward(ThreadType(ThreadLevel.TWO, Extense.OPEN, True), True)]
        self.assertEqual(self.sb_1.case_same_type(P.BLACK, cp1, cp2), expected)
    
    def test_case_same_type2(self):
        cp1 = (P.BLACK, 2, False)
        cp2 = (P.BLACK, 1, True)
        expected = [Reward(ThreadType(ThreadLevel.THREE, Extense.HALF_OPEN, True), True)]
        self.assertEqual(self.sb_1.case_same_type(P.BLACK, cp1, cp2), expected)

    def test_case_same_type3(self):
        cp1 = (P.BLACK, 2, False)
        cp2 = (P.BLACK, 1, False)
        expected = [Reward(ThreadType(ThreadLevel.THREE, Extense.CLOSED, True), True)]
        self.assertEqual(self.sb_1.case_same_type(P.BLACK, cp1, cp2), expected)

    def test_case_different_type(self):
        cp1 = (P.BLACK, 2, True)
        cp2 = (P.WHITE, 2, True)
        expected = [Reward(ThreadType(ThreadLevel.TWO, Extense.HALF_OPEN, False), True),
                    Reward(ThreadType(ThreadLevel.TWO, Extense.HALF_OPEN, False), False)]
        self.assertEqual(self.sb_1.case_different_type(P.BLACK, cp1, cp2), expected)

    
    def test_case_different_type2(self):
        cp1 = (P.BLACK, 2, False)
        cp2 = (P.WHITE, 3, True)
        expected = [Reward(ThreadType(ThreadLevel.TWO, Extense.CLOSED, False), False),
                    Reward(ThreadType(ThreadLevel.THREE, Extense.HALF_OPEN, False), True)]
        self.assertEqual(self.sb_1.case_different_type(P.WHITE, cp1, cp2), expected)

    def test_case_different_type3(self):
        cp1 = (P.BLACK, 3, False)
        cp2 = (P.WHITE, 3, False)
        expected = [Reward(ThreadType(ThreadLevel.THREE, Extense.CLOSED, False), False),
                    Reward(ThreadType(ThreadLevel.THREE, Extense.CLOSED, False), True)]
        self.assertEqual(self.sb_1.case_different_type(P.WHITE, cp1, cp2), expected)

    def test_dir_rewards_empty(self):
        expected = [Reward(ThreadType(ThreadLevel.THREE, Extense.HALF_OPEN, True), True)]
        self.assertEqual(self.sb_2.dir_rewards(P.WHITE, 0, 12, D.RIGHT), expected)

    def test_dir_rewards_same_type(self):
        self.assertEqual(self.sb_2.dir_rewards(P.BLACK, 0, 6, D.RIGHT), 
            [Reward(ThreadType(ThreadLevel.TWO, Extense.HALF_OPEN, True), True)])
    
    def test_dir_rewards_different_type(self):
        self.assertEqual(self.sb_2.dir_rewards(P.BLACK, 0, 5, D.RIGHT), 
            [Reward(ThreadType(ThreadLevel.TWO, Extense.HALF_OPEN, False), False),
            Reward(ThreadType(ThreadLevel.TWO, Extense.HALF_OPEN, False), True)])