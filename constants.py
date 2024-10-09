# players
from enum import Enum

AI = "AI"
USER = "USER"
VALID_PLAYERS = [
    AI,
    USER
]


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


# dimensions
BLOCK_SIZE = 20
SPEED = 5
BOARD_HEIGHT = 35
BOARD_LENGTH = 20


class GameState(Enum):
    GAME_OVER = -10
    PLAYING = 0


class Color(Enum):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 192, 0)
    BLUE = (0, 32, 255)
    YELLOW = (255, 224, 32)
    ORANGE = (255, 160, 16)
    PURPLE = (160, 32, 255)
    GRAY = (128, 128, 128)
    PINK = (255, 96, 208)

