from typing import List
import pygame
from constants import *
from tetrominoes import Tetromino, random_tetromino


class Tetris:
    def __init__(self):
        self.score: int = 0
        self.max_height: int = 0
        self.board: List[List] = [[None]*BOARD_LENGTH for _ in range(BOARD_HEIGHT)]
        pygame.init()
        self.font = pygame.font.Font('assets/fonts/arial.ttf', 25)
        self.length_pix: int = BOARD_LENGTH * BLOCK_SIZE + 8*BLOCK_SIZE
        self.height_pix: int = BOARD_HEIGHT*BLOCK_SIZE
        self.display = pygame.display.set_mode((self.length_pix, self.height_pix))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.frame_iteration: int = 0
        logo = pygame.image.load('assets/logo.png')
        pygame.display.set_icon(logo)
        self.new_tetromino: Tetromino = None
        # colors
        self.bg_color = Color.WHITE.value
        self.score_color = Color.BLACK.value
        self.line_separation_color = Color.RED.value
        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.max_height = 0
        self.board = [[None] * BOARD_LENGTH for _ in range(BOARD_HEIGHT)]
        self.frame_iteration = 0
        self.new_tetromino = None

    def spawn_tetromino(self) -> Tetromino:
        return random_tetromino((int(BOARD_LENGTH/2), 0))

    def update(self, direction, rotate):
        if self.new_tetromino is None:
            self.new_tetromino = self.spawn_tetromino()
        self.new_tetromino.pos = (self.new_tetromino.pos[0], self.new_tetromino.pos[1]+1)

    def update_ui(self) -> None:
        # clear the screen
        self.display.fill(self.bg_color)
        # draw separation line
        half_length = int(BOARD_LENGTH*BLOCK_SIZE + BLOCK_SIZE/2)
        pygame.draw.line(self.display, self.line_separation_color, (half_length, 0), (half_length, self.height_pix))
        # draw board
        self.draw_board()
        # draw new tetromino
        new_t = self.new_tetromino
        size = len(new_t.shape)
        for i in range(size):
            for j in range(size):
                if new_t.shape[i][j] == 1:
                    self.draw_block(x=(new_t.pos[0] + i)*BLOCK_SIZE, y=(new_t.pos[1] + j)*BLOCK_SIZE, color=new_t.color)
        # score
        text = self.font.render(f'Score', True, self.score_color)
        self.display.blit(text, ((BOARD_LENGTH+2)*BLOCK_SIZE, BLOCK_SIZE*2))
        text = self.font.render(f'{self.score}', True, self.score_color)
        self.display.blit(text, ((BOARD_LENGTH+2)*BLOCK_SIZE, BLOCK_SIZE*4))
        # update the window
        pygame.display.flip()

    def draw_board(self) -> None:
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_LENGTH):
                color = self.board[i][j]
                if color is not None:
                    self.draw_block(i*BLOCK_SIZE, j*BLOCK_SIZE, color)

    def draw_block(self, x, y, color):
        border_size = 1
        pygame.draw.rect(self.display, Color.BLACK.value, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, color.value,
                         pygame.Rect(x+border_size, y+border_size, BLOCK_SIZE-border_size*2, BLOCK_SIZE-border_size*2))
