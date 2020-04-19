import pygame
from pygame.locals import *
import sys
import random
from gameState import GameState
from piece import Piece
from player import Player
from qlearningAgent import ApproximateQAgent

canvasWidth = 900
canvasHeight = 645

lineWidth = 1
lineWidth2 = 4
lineWidth3 = 4
boxWidth = 40

marginWidth = 24

N = 15
n_win = 5

boardWidth = lineWidth * N + boxWidth * (N - 1)

starty = (canvasHeight - boardWidth) / 2
startx = starty

cpSize = 29

address = '../resources/'
img_board = pygame.image.load(address + 'board.png')
img_white = pygame.image.load(address + 'cp_w_29.png')
img_black = pygame.image.load(address + 'cp_k_29.png')
gameDisplay = pygame.display.set_mode((canvasWidth, canvasHeight))



def main():
    """
    Here is the main of the entire program where the pygame is
    initialized properly.
    """
    pygame.init()
    pygame.display.set_caption("Gomuku")
    gameDisplay.blit(img_board, (0, 0))
    pygame.display.update()

    playerOneType = Player.HUMAN
    playerTwoType = Player.AI

    curPlayer = Piece.WHITE  # first player is always BLACK

    hasWinner = Piece.EMPTY
    gameState = GameState()
    board = gameState.board
    board[7][7] = Piece.BLACK
    renderPiece((7, 7), Piece.BLACK)
    pygame.display.update()
    qAgent = ApproximateQAgent(Piece.WHITE)
    qAgent.startEpisode()
    numEpisodes = 12

    while True:
        while hasWinner == Piece.EMPTY and numEpisodes > 0:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                    pygame.quit()
                    exit()
            # delegate to players
            if curPlayer == Piece.BLACK and playerOneType == Player.HUMAN:
                row, col = getPiecePos()
                while not isValid((row, col), board):
                    row, col = getPiecePos()
                board[row][col] = curPlayer
            elif curPlayer == Piece.BLACK and playerOneType == Player.AI:
                # action = qAgent.getAction(gameState)
                # row, col = action
                # oldState = gameState
                # board[row][col] = curPlayer
                # qAgent.update(oldState, action, gameState, oldState.getScore(curPlayer, action))
                row, col = random.sample(gameState.getPossibleMoves(), 1)[0]
            elif curPlayer == Piece.WHITE and playerTwoType == Player.HUMAN:
                row, col = getPiecePos()
                while not isValid((row, col), board):
                    row, col = getPiecePos()
                board[row][col] = curPlayer
            elif curPlayer == Piece.WHITE and playerTwoType == Player.AI:
                action = qAgent.getAction(gameState)
                row, col = action
                oldState = gameState
                board[row][col] = curPlayer
                qAgent.update(oldState, action, gameState, oldState.getScore(curPlayer, action))
                print(qAgent.getWeights())

            renderPiece((row, col), curPlayer)
            pygame.display.update()
            hasWinner = checkIfWins(board)

            if hasWinner != Piece.EMPTY:
                print("Finish episode", numEpisodes)
                numEpisodes -= 1

                if hasWinner == Piece.BLACK:
                    print ("Black wins")
                elif hasWinner == Piece.WHITE:
                    print ("White wins")

                qAgent.stopEpisode()
                gameDisplay.blit(img_board, (0, 0))
                pygame.display.update()
                hasWinner = Piece.EMPTY
                gameState.resetBoard()
                board = gameState.board
                board[7][7] = Piece.BLACK
                renderPiece((7, 7), Piece.BLACK)
                curPlayer = Piece.WHITE
                pygame.display.update()
                continue
                # sys.exit()
                # pygame.quit()
                # exit()

            curPlayer = Piece.takeTurn(curPlayer)


def isValid(pos, board):
    """
    Checks if the pos on the current board is occupied with
    a player's piece. If yes, the pos is invalid, otherwise valid.

    :param pos: a tuple consist of (row, col)
    :param board: 15 by 15 2-D lists
    :return: whether or no the pos is valid
    """
    row = pos[0]
    col = pos[1]
    if row < 0 or row > N - 1:
        return False
    elif col < 0 or col > N - 1:
        return False

    return board[row][col] == Piece.EMPTY


def checkIfWins(board):
    """
    Checks if the player's last move leads to a wining state

    :param board: the 2D array of pieces
    :return: the player type if it won
    """
    directions = ((1, -1), (1, 0), (1, 1), (0, 1))
    for row in range(15):
        for col in range(15):
            if board[row][col] == Piece.EMPTY: continue
            id = board[row][col]
            for d in directions:
                x, y = row, col
                count = 0
                while count < 5:
                    if board[x][y] != id: break
                    x += d[0]
                    y += d[1]
                    count += 1
                    if x > 14 or x < 0 or y > 14 or y < 0: break
                if count == 5:
                    return id
    return Piece.EMPTY


def renderPiece(pos, player):
    """
    Render the piece on the canvas based on current player type.

    :param pos: a tuple consist of (row, col)
    :param player: the current player type: one of WHITE or BLACK
    """
    x = startx + lineWidth / 2 + pos[1] * (lineWidth + boxWidth) - (cpSize - 1) / 2
    y = starty + lineWidth / 2 + pos[0] * (lineWidth + boxWidth) - (cpSize - 1) / 2

    if player == Piece.BLACK:
        gameDisplay.blit(img_black, (x, y))
    else:
        gameDisplay.blit(img_white, (x, y))


def getPiecePos():
    """
    Gets a approximate location of the mouse click, rounding to a closest
    piece on the chessboard.

    :return: the position of the piece on the chessboard
    """
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
                exit()
            elif e.type == MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                row = int(round((y - starty - lineWidth / 2.0) / (lineWidth + boxWidth)))
                col = int(round((x - startx - lineWidth / 2.0) / (lineWidth + boxWidth)))
                return row, col


if __name__ == '__main__':
    main()
