from piece import Piece
import util
from board import Board
from copy import copy, deepcopy
from operator import add, sub
from enum import Enum

class Directions(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    DOWN_RIGHT = (1, 1)
    UP_RIGHT = (-1, 1)

    ALL_DIRECTIONS = (RIGHT, DOWN, DOWN_RIGHT, UP_RIGHT)

class GameState:
    """
    Represents a 15 by 15 chessboard.
       a b c d e f g h i j k l m n o
    a' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    b' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    c' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    d' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    e' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    f' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    g' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    h' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    i' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    j' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    k' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    l' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    m' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    n' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    o' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
    """
    def __init__(self):
        # fill the board with Empty pieces
        self.board = Board()
        self.directions = Directions.ALL_DIRECTIONS

    def get_threat(self, pieceType, row, col):
        """ return a list of thread according to the newly placed piece
        
        Arguments:
            pieceType {Piece} -- either WHITE or BLACK
            row {int} -- the row of newly placed piece
            col {[type]} -- the column of newly placed piece

        Returns:
            List of Thread -- Thread is (Thread_type, pieces_pos) where peces_pos
                is a list of pos tuples.
        """
        threads = []
        for dir in Directions.ALL_DIRECTIONS:
            pos = (row, col)
            subtract = (dir.value[0] * 5, dir.value[1] * 5)
            pos = map(sub, pos, subtract)
            thread = []
            cur_state = 0
            for i in range(10):
                if self.board.verify_pos(pos[0], pos[1]):
                    type = self.board.get_piece_type(pos)
                    if type == pieceType:
                        thread.append(pos)
                    elif type == Piece.EMPTY and cur_state == 0:
                        cur_state += 1
                    elif type == Piece.EMPTY and broken:
                        thread_type = 
                else:
                    pos = map(add, pos, dir.value)

    def id_thread(self, thread, broken):
        """ return a thread type by identifying the given thread
        
        Arguments:
            thread {list} -- list of pos
        """
        


    def getScore(self, pieceType, action):
        totalScore = 0
        consecutivePiecesMap = self.getConsecutivePiecesMap(action, pieceType)
        consecutivePieces = consecutivePiecesMap.values()
        consecutivePiecesCount = [item[0] for item in consecutivePieces]

        print(consecutivePiecesCount)
        if 2 in consecutivePiecesCount:
            totalScore += 2
        if 3 in consecutivePiecesCount:
            totalScore += 10
        if 4 in consecutivePiecesCount:
            totalScore += 20
        if 5 in consecutivePiecesCount:
            totalScore += 999

        if self.recognizeThreat(pieceType, action, 3, True) == None:
            totalScore += 200
        if self.recognizeThreat(pieceType, action, 4, False) == None:
            totalScore += 200
        if self.recognizeThreat(pieceType, action, 5, False) != None:
            return -1000
        print(totalScore)
        return totalScore

    # def doAction(self, pieceType, pos):
    #     self.board


class Agent:
    def __init__(self, pieceType):
        self.pieceType = pieceType

    def getAction(self, state):
        util.raiseNotDefined()

class ReinforcementAgent(Agent):
    def __init__(self, pieceType, numTraining=100, epsilon=0.5, alpha=0.5, gamma=1):
        Agent.__init__(self, pieceType)
        self.episodesSoFar = 0
        self.episodeRewards = 0.0
        self.accumTrainRewards = 0.0
        self.accumTestRewards = 0.0
        self.numTraining = int(numTraining)
        self.epsilon = int(epsilon)
        self.alpha = float(alpha)
        self.discount = float(gamma)

    def getQValue(self, state, action):
        util.raiseNotDefined()

    def getPolicy(self, state):
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        util.raiseNotDefined()

    def getLegalActions(self, state):
        return state.getPossibleMoves()

    def startEpisode(self):
        self.episodeRewards == 0.0

    def stopEpisode(self):
        if self.episodesSoFar < self.numTraining:
            self.accumTrainRewards += self.episodeRewards
        else:
            self.accumTestRewards += self.episodeRewards
        self.episodesSoFar += 1
        if self.episodesSoFar >= self.numTraining:
            self.epsilon = 0.0  # no exploration
            self.alpha = 0.0  # no learning

    def isInTraining(self):
        return self.episodesSoFar < self.numTraining

    def isInTesting(self):
        return not self.isInTraining()

    def observeTransitions(self, state, action, nextState, deltaReward):
        self.episodeRewards += deltaReward
        self.update(state, action, nextState, deltaReward)