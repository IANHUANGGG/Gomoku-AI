import util
from piece import Piece

class FeatureExtractor:
    """
    This class represents the public API should be
    supported by a feature extractor.
    """
    def getFeatures(state, pos, pieceType):
        util.raiseNotDefined()


class SimpleExtractor(FeatureExtractor):
    def getFeatures(state, pos, pieceType):
        features = util.Counter()
        features["bias"] = 1.0

        consecutivePiecesMap = state.getConsecutivePiecesMap(pos, pieceType)
        consecutivePieces = consecutivePiecesMap.values()
        consecutivePiecesCount = [item[0] for item in consecutivePieces]
        if 3 in consecutivePiecesCount:
            features["three-in-a-row"] = 1.0
        if 4 in consecutivePiecesCount:
            features["four-in-a-row"] = 2.0
        if 5 in consecutivePiecesCount:
            features["five-in-a-row"] = 3.0
        if state.recognizeThreat(pieceType, pos, 3, True) == None:
            features["opponent-three-in-a-row"] = 3.0
        if state.recognizeThreat(pieceType, pos, 4, False) == None:
            features["opponent-four-in-a-row"] = 4.0

        # features["num-of-consecutive"] = len([num for num in lineList if num > 1])
        features.divideAll(10.0)

        return features