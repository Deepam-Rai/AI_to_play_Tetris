import random
from enum import Enum
from utils import Color


class TetrominoType(Enum):
    I = ([[1], [1], [1], [1]], Color.BLUE)
    O = ([[1, 1], [1, 1]], Color.YELLOW)
    T = ([[1, 1, 1], [0, 1, 0], [0, 1, 0]], Color.PURPLE)
    J = ([[0, 1], [0, 1], [1, 1]], Color.BLUE)
    L = ([[1, 0], [1, 0], [1, 1]], Color.ORANGE)
    S = ([[0, 1, 1], [1, 1, 0]], Color.GREEN)
    Z = ([[1, 1, 0], [0, 1, 1]], Color.RED)


class Tetromino:
    def __init__(self, tetromino_type: TetrominoType):
        self.shape = tetromino_type.value[0]
        self.color = tetromino_type.value[1]

    def rotate(self) -> None:
        """
        Rotates the shape clockwise 90 degrees.
        :return:
        """
        self.shape = list(map(list, zip(*self.shape[::-1])))


def random_tetromino() -> Tetromino:
    return Tetromino(random.choice(list(TetrominoType)))


if __name__ == "__main__":
    t = random_tetromino()
    print(t.shape)
    t.rotate()
    print(t.shape)
