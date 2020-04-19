from enum import Enum

class Direction(Enum):
    RIGHT = (0, 1)
    DOWN = (1, 0)
    DOWN_RIGHT = (1, 1)
    UP_RIGHT = (-1, 1)

    ALL_DIRECTIONS = (RIGHT, DOWN, DOWN_RIGHT, UP_RIGHT)