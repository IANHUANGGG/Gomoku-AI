from gameState import Agent
import util

def evaluationFunction():
    return 0

class MinimaxAgent(Agent):
    def __init__(self, evalFn = 'evaluationFunction', depth = 2):
        self.evaluator = util.lookup(evalFn, globals())
        self.depth = depth

    """
    Represents a minimax agent with alph-beta pruning
    """
    def getAction(self, state):
        """
        Figure out an optimal move based on current game state, specifically
        the board state.

        :param state: the current board state
        :return: a position of the chess board which is optimal
        """
        possibleMoves = state.getPossibleMoves()
        return possibleMoves[0]