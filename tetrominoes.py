import random
from enum import Enum
from typing import Tuple
from constants import Color


class TetrominoType(Enum):
    I = ([
             [0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]
         ], Color.BLUE)
    O = ([
             [0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]
         ], Color.YELLOW)
    T = ([
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 0, 0, 0]
         ], Color.PURPLE)
    J = ([
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]
         ], Color.BLUE)
    L = ([
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]
         ], Color.ORANGE)
    S = ([
             [0, 0, 0, 0],
             [0, 1, 1, 0],
             [1, 1, 0, 0],
             [0, 0, 0, 0],
         ], Color.GREEN)
    Z = ([
             [0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]
         ], Color.RED)


class Tetromino:
    def __init__(self, tetromino_type: TetrominoType, pos: Tuple):
        self.shape = tetromino_type.value[0]
        self.color = tetromino_type.value[1]
        self.pos = pos

    def rotate(self) -> None:
        """
        Rotates the shape clockwise 90 degrees.
        :return:
        """
        self.shape = list(map(list, zip(*self.shape[::-1])))

    def opp_rotate(self) -> None:
        self.shape = list(map(list, zip(*[row[::-1] for row in self.shape])))


def random_tetromino(pos: Tuple) -> Tetromino:
    return Tetromino(random.choice(list(TetrominoType)), pos)


if __name__ == "__main__":
    def show(tetromino):
        print()
        for row in tetromino.shape:
            for block in row:
                print(block, end="")
            print()
    t = random_tetromino((0,0))
    show(t)
    t.rotate()
    show(t)
    t.opp_rotate()
    show(t)
