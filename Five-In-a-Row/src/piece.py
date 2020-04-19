class Piece:
    """
    Three types of pieces:
    EMPTY - no piece yet
    BLACK - the black piece
    WHITE - the white piece
    """
    EMPTY = -1
    BLACK = 0
    WHITE = 1

    def takeTurn(lastPlayerType):
        if lastPlayerType == Piece.BLACK:
            return Piece.WHITE
        elif lastPlayerType == Piece.WHITE:
            return Piece.BLACK