from src.piece import Piece
import src.util
import src.constant as cons
import copy

class Board:
    def __init__(self):
        self.board = [[Piece.EMPTY for col in range(cons.NORMAL_B_HEIGHT)] for row in range(cons.NORMAL_B_WIDTH)]
        self.height = cons.NORMAL_B_HEIGHT
        self.width = cons.NORMAL_B_WIDTH

    def resetBoard(self):
        """ Reset the Board to empty
        """

        self.board = [[Piece.EMPTY for col in range(15)] for row in range(15)]

    def getBoard(self):
        """ return a copy of the board
        """
        return copy.deepcopy(self.board)

    def place_piece(self, piece, row, col):
        """ return true if placed a piece on the board successfully
        
        Arguments:
            piece {Piece} -- either EMPTY, WHITE, or BLACK
        """
        
        return self.board[row][col]


    def piece_type(self, row, col):
        return self.board[row][col]


    def verify_pos(self, row, col):
        """ verify if the given position is on the board, and return True if on the board

        Arguments:
            row {int} -- the row
            col {int} -- the column
        
        Returns:
            bool - if the given position is valid in the chess board
        """
        return (row >= 0 and col >= 0 and 
            row < self.height and col < self.width)
        
    def if_on_boundary(self, row, col, dir, func):
        """ check if a piece can be placed at the posotion where is one slot further in the direction
            of the given position. 
        
        Returns:
            [bool] -- True if the position is already on the boundary
        """
        pos = tuple(map(func, (row, col), dir.value))
        return not self.verify_pos(pos[0], pos[1])
