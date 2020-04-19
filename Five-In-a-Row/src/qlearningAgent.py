from gameState import ReinforcementAgent
import util
import sys
import random
from featureExtractors import *

class ApproximateQAgent(ReinforcementAgent):
    def __init__(self, pieceType, extractor='SimpleExtractor'):
        ReinforcementAgent.__init__(self, pieceType)
        self.featExtractor = util.lookup(extractor, globals())
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
        Calculate the Q value of the state action pair.
        In approximate Q-learning, we comply the formula
        Q(state, action) = w * featureVectors

        :param state: the current game state
        :param action: a valid position on the board
        :return: a q-value of the state action pair
        """
        return self.weights * self.featExtractor.getFeatures(state, action, self.pieceType)

    def computeValueFromQValue(self, state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return 0.0
        else:
            maxQValue = -sys.maxsize - 1
            for action in actions:
                maxQValue = max(maxQValue, self.getQValue(state, action))

        return maxQValue

    def computeActionFromQValue(self, state):
        actions = self.getLegalActions(state)
        if len(actions) == 0:
            return None
        else:
            bestAction = None
            maxQValue = - sys.maxsize - 1
            for action in actions:
                # print("we have action", action, self.getQValue(state, action))
                if self.getQValue(state, action) > maxQValue:
                    maxQValue = self.getQValue(state, action)
                    bestAction = action

        print("We finally chose", bestAction, self.getQValue(state, bestAction))
        return bestAction

    def getAction(self, state):
        legalActions = self.getLegalActions(state)
        exploration = util.flipCoin(self.epsilon)
        if exploration == True:
            return random.choice(legalActions)
        else:
            return self.computeActionFromQValue(state)

    def update(self, state, action, nextState, reward):
        curQValue = self.getQValue(state, action)
        newQValue = reward + self.discount * self.getValue(nextState)
        difference = newQValue - curQValue

        features = self.featExtractor.getFeatures(state, action, self.pieceType)
        for feature in features:
            curFeature = self.featExtractor.getFeatures(state, action, self.pieceType)[feature]
            self.weights[feature] = self.weights[feature] + self.alpha * difference * curFeature

    def getPolicy(self, state):
        return self.computeActionFromQValue(state)

    def getValue(self, state):
        return self.computeValueFromQValue(state)


