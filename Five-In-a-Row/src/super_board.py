from src.thread import ThreadType, ThreadLevel, Extense, Reward
from src.board import Board
from src.direction import Direction
from operator import add, sub
from src.piece import Piece

class SuperBoard(Board):

    def __init__(self, board=None):
        super().__init__()
        if board != None:
            self.board = board
            self.height = len(board)
            self.width = len(board[0])
        self.valued_moves = set((7,7))
        self.winner = None
        """
         score represent the how much advantage one player has over the other player in terms of current 
         game state. When score is positive, Black has advantage over White, otherwise White is in advantage
        """
        self.reward = 0
        self.score = 0

    def place_piece(self, piece, row, col):
        """ Place a piece on the board and update the valued moves
        
        Arguments:
            piece [Piece] -- either EMPTY, WHITE, or BLACK
            row [int] -- row
            col [int] -- column
        """
        if self.board.verify_pos(row, col):
            rewards = self.create_rewards(piece, row, col)
            #TODO: delete the pos from valued_moves
            self.check_game_end(piece, rewards)
            super().place_piece(piece, row, col)
            self.update_moves(row, col)

    def check_game_end(self, piece, rewards):
        """ set winner if the game is ended
        """
        if ThreadLevel.FIVE in rewards:
            self.winner = piece
            return True
        return False
        #TODO fix

    def get_winner(self):
        """ Return the winner
        
        Returns:
            [Piece] -- [the winner]
        """

        return self.winner

    def get_score(self, piece, row, col):
        """ return the current score
        
        Arguments:
            piece {[type]} -- [description]
            row {[type]} -- [description]
            col {[type]} -- [description]
        """
        return self.score

    def create_rewards(self, piece, row, col):
        """ return a list of thread according to the newly placed piece

        Arguments:
            pieceType {Piece} -- either WHITE or BLACK
            row {int} -- the row of newly placed piece
            col {[type]} -- the column of newly placed piece

        Returns:
            List of rewards
        """
        rewards = []
        for dir in Direction.ALL_DIRECTIONS:
            rewards = rewards + (self.dir_rewards(piece, row, col, dir))
        return rewards

        
    def dir_rewards(self, piece, row, col, dir):
        """ returns a list of expected rewards by placing the piece at given position in certain direction
        
        Arguments:
            piece {[type]} -- [description]
            row {[type]} -- [description]
            col {[type]} -- [description]
            dir {[type]} -- [description]

        Returns:
            List of Rewards 
        """
        consecutive_p1 = self.consecutive_pieces(row, col, dir, sub)
        consecutive_p2 = self.consecutive_pieces(row, col, dir, add)
        if consecutive_p1[0] == Piece.EMPTY:
            return self.case_indiv(piece, consecutive_p2)
        if consecutive_p2[0] == Piece.EMPTY:
            return self.case_indiv(piece, consecutive_p1)
        if consecutive_p1[0] == consecutive_p2[0]:
            return self.case_same_type(piece, consecutive_p1, consecutive_p2)
        return self.case_different_type(piece, consecutive_p1, consecutive_p2)


    def case_indiv(self, piece, consecutive_p, open_end=True):
        """ Create and return the reward by only looking at only one set of consecutive pieces
        
        Arguments:
            piece {Piece} -- Black or White, Empty is prohibited in this case
            consecutive_p {tuple} -- (piece_type, len, open)
        
        Keyword Arguments:
            open_end {bool} -- [If the other end is open or not] (default: {True})
        
        Returns:
            List of Rewards
        """

        if consecutive_p[0] == Piece.EMPTY:
            return []
        else:
            thread_level = ThreadLevel.get_thread_level(consecutive_p[1])
            extense = Extense.get_extense(consecutive_p[2], open_end, consecutive_p[1])
            thread_type = ThreadType(thread_level, extense, False)
            return [Reward(thread_type, piece == consecutive_p[0])]

    def case_same_type(self, piece, cp1, cp2):
        """ Create and return the rewards by looking at two sets of consecutive pieces and 
            the piece of two sets are the same
        
        case_same_type should alway create thread_type where broken is True
        cp1 and cp2 always have the same piece in this case
        
        Arguments:
            piece {Piece} -- Black or White, Empty is prohibited in this case
            cp1 {tuple} -- (piece_type, len, open)
            cp2 {tuple} -- (piece_type, len, open)
        
        Returns:
            List of Rewards
        """

        level = ThreadLevel.get_thread_level(cp1[1] + cp2[1])
        extense = Extense.get_extense(cp1[2], cp2[2], cp1[1] + cp2[1])
        broken = True
        thread_type = ThreadType(level, extense, broken)
        return [Reward(thread_type, piece == cp1[0])]

    def case_different_type(self, piece, cp1, cp2):

        thread_list1 = self.case_indiv(piece, cp1, False)
        thread_list2 = self.case_indiv(piece, cp2, False)
        return thread_list1 + thread_list2
        
             
    def consecutive_pieces(self, row, col, dir, func):
        """ 
        
        Arguments:
            row {int} -- the y position
            col {int} -- the x position
            dir {Direction} -- the direction
            func {function} -- either add or sub
        
        Returns:
            tuple -- (piece_type, len, open)
                where len is int and open is a bool
        """

        if not self.verify_pos(row, col): raise ValueError("passed in an invalid position")
        pos = (row, col)
        consecutive_type = Piece.EMPTY
        len = 0
        for num in range(1, 5):
            pos = tuple(map(func, pos, dir.value))
            piece = self.piece_type(pos[0], pos[1])
            if piece == Piece.EMPTY: return (consecutive_type, len, True)
            if consecutive_type == Piece.EMPTY:
                consecutive_type = piece
                len += 1
            else:
                if consecutive_type == piece: 
                    len += 1
                else: return (consecutive_type, len, False)
            if self.if_on_boundary(pos[0], pos[1], dir, func): 
                return (consecutive_type, len, False)  
                

    def calc_reward_point(self, piece, rewards):
        """ Given a list of rewards, calculate and return the points for the rewards
        
        Arguments:
            piece {Piece} -- Either WHITE or BLACK
            rewards {List of Rewards}

        Returns:
            int -- reward points
        """

        # for reward in rewards:



    def get_v_moves(self):
        """ return a set of useful moves according to the current game state
        
        Returns:
            set -- the possible useful moves
        """
        return self.valued_moves

    def update_moves(self, row, col):
        """ Update the available slots according to the newly occupied slot
        
        Arguments:
            row {int} -- the row number
            col {int} -- the column number
        """
        for dir in Direction.ALL_DIRECTIONS:
            self.update_moves_dir(row, col, dir, sub)
            self.update_moves_dir(row, col, dir, add)
        self.valued_moves.remove((row, col))

    def update_moves_dir(self, row, col, dir, func):
        pos = (row, col)
        for i in range(1, 3):
            pos = tuple(map(func, pos, dir.value))
            if (self.verify_pos(pos[0], pos[1]) and self.piece_type(pos[0], pos[1]) == Piece.EMPTY and
                pos not in self.valued_moves):
                self.valued_moves.add(pos)

#TODO thread dict
#TODO board version