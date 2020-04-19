from enum import Enum

class Reward():
    
    def __init__(self, thread_type, same_piece):
        self.thread_type = thread_type
        # same_piece is bool
        self.same_piece = same_piece

    def __eq__(self, other):
        return self.thread_type == other.thread_type and self.same_piece == other.same_piece

    def __repr__(self):
        return "thread_type: " + self.thread_type.__repr__() + ". same_piece: " + str(self.same_piece)


class ThreadType:

    def __init__(self, thread_level, extense, broken):
        self.thread_level = thread_level
        self.extense = extense
        self.broken = broken

    def __eq__(self, other):
        return (self.thread_level == other.thread_level and
                self.extense == other.extense and 
                self.broken == other.broken)
    
    def __repr__(self):
        return self.thread_level.name + " " + self.extense.name + " " + str(self.broken)

class ThreadLevel(Enum):
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    NOT_THREAD = 0

    @staticmethod
    def get_thread_level(num):
        if num >= 5: return ThreadLevel.FIVE
        return CONSECUTIVE_DICT[num]

class Extense(Enum):
    OPEN = 1
    HALF_OPEN = 2
    CLOSED = 3

    @staticmethod
    def get_extense(open1, open2, len=None):
        if open1 and open2:
            return Extense.OPEN
        if not (open1 or open2):
            if len == 4:
                return Extense.HALF_OPEN
            else:
                return Extense.CLOSED
        return Extense.HALF_OPEN

CONSECUTIVE_DICT = {0: ThreadLevel.NOT_THREAD, 1: ThreadLevel.NOT_THREAD, 2: ThreadLevel.TWO, 
                    3: ThreadLevel.THREE, 4: ThreadLevel.FOUR, 5: ThreadLevel.FIVE}
