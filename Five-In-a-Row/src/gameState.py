from piece import Piece
import util
from copy import copy, deepcopy

class Directions:
    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)
    UP_LEFT = (-1, -1)
    DOWN_RIGHT = (1, 1)
    UP_RIGHT = (-1, 1)
    DOWN_LEFT = (1, -1)

    ALL_DIRECTIONS = (LEFT, RIGHT, UP, DOWN, UP_LEFT, DOWN_RIGHT, UP_RIGHT, DOWN_LEFT)

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
        self.board = [[Piece.EMPTY for col in range(15)] for row in range(15)]
        self.directions = Directions.ALL_DIRECTIONS

    def resetBoard(self):
        self.board = [[Piece.EMPTY for col in range(15)] for row in range(15)]

    def getPossibleMoves(self):
        avaliableSlots = set()
        for row in range(15):
            for col in range(15):
                id = self.board[row][col]
                if id == Piece.EMPTY: continue
                for d in self.directions:
                    x, y = row, col
                    for i in range(1):
                        x += d[0]
                        y += d[1]
                        if x > 14 or x < 0 or y > 14 or y < 0: break
                        if self.board[x][y] == Piece.EMPTY:
                            avaliableSlots.add((x, y))
        return avaliableSlots

    def getConsecutivePiecesMap(self, pos, pieceType):
        directions = Directions.ALL_DIRECTIONS
        row = pos[0]
        col = pos[1]
        consecutivePieces = util.Counter()

        for d in directions:
            x, y = row, col
            count = 1
            pieces = []
            while count < 5:
                x += d[0]
                y += d[1]
                if x > 14 or x < 0 or y > 14 or y < 0: break
                if self.board[x][y] != pieceType: break
                pieces.append((x, y))
                count += 1
            consecutivePieces[d] = pieces

        leftBranch = consecutivePieces[(0, -1)]
        leftBranch.reverse()
        rightBranch = consecutivePieces[(0, 1)]

        upBranch = consecutivePieces[(-1, 0)]
        upBranch.reverse()
        downBranch = consecutivePieces[(1, 0)]

        upLeftBranch = consecutivePieces[(-1, -1)]
        upLeftBranch.reverse()
        downRightBranch = consecutivePieces[(1, 1)]

        downLeftBranch = consecutivePieces[(1, -1)]
        downLeftBranch.reverse()
        upRightBranch = consecutivePieces[(-1, 1)]

        horizontal = leftBranch + [pos] + rightBranch
        vertical = upBranch + [pos] + downBranch
        diag_down = upLeftBranch + [pos] + downRightBranch
        diag_up = downLeftBranch + [pos] + upRightBranch

        result = {"horizontal" : (len(horizontal), horizontal),
                  "vertical" : (len(vertical), vertical),
                  "diag_down" : (len(diag_down), diag_down),
                  "diag_up" : (len(diag_up), diag_up)}

        return result

    def recognizeThreat(self, pieceType, action, num, twoSided):
        newBoard = deepcopy(self.board)
        newBoard[action[0]][action[1]] = pieceType
        opponentPieceType = Piece.takeTurn(pieceType)
        for row in range(15):
            for col in range(15):
                id = self.board[row][col]
                if id == opponentPieceType:
                    consecutivePiecesMap = self.getConsecutivePiecesMap((row, col), opponentPieceType)
                    for key, value in consecutivePiecesMap.items():
                        if value[0] != num: continue
                        line = value[1]
                        l_x, l_y = line[0]
                        r_x, r_y = line[num - 1]
                        if key == "horizontal":
                            l_x += Directions.LEFT[0]
                            l_y += Directions.LEFT[1]
                            r_x += Directions.RIGHT[0]
                            r_y += Directions.RIGHT[1]
                        elif key == "vertical":
                            l_x += Directions.UP[0]
                            l_y += Directions.UP[1]
                            r_x += Directions.DOWN[0]
                            r_y += Directions.DOWN[1]
                        elif key == "diag_down":
                            l_x += Directions.UP_LEFT[0]
                            l_y += Directions.UP_LEFT[1]
                            r_x += Directions.DOWN_RIGHT[0]
                            r_y += Directions.DOWN_RIGHT[1]
                        elif key == "diag_up":
                            l_x += Directions.DOWN_LEFT[0]
                            l_y += Directions.DOWN_LEFT[1]
                            r_x += Directions.UP_RIGHT[0]
                            r_y += Directions.UP_RIGHT[1]
                        if l_x > 14 or l_x < 0 or l_y > 14 or l_y < 0 or \
                                r_x > 14 or r_x < 0 or r_y > 14 or r_y < 0: break
                        if twoSided:
                            if newBoard[l_x][l_y] == Piece.EMPTY and newBoard[r_x][r_y] == Piece.EMPTY:
                                return ((l_x, l_y), (r_x, r_y))
                        else:
                            if newBoard[l_x][l_y] == Piece.EMPTY:
                                return (l_x, l_y)
                            if newBoard[r_x][r_y] == Piece.EMPTY:
                                return (r_x, r_y)
        return None


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