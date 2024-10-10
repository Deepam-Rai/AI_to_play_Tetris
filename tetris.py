from typing import List
import pygame
from constants import *
from tetrominoes import Tetromino, random_tetromino


class Tetris:
    def __init__(self):
        self.score: int = 0
        self.lines_cleared: int = 0
        self.consecutive: int = 0
        self.game_state = GameState.PLAYING
        self.level = 1
        self.speed = self.level * BASE_SPEED
        self.board: List[List] = [[None]*BOARD_LENGTH for _ in range(BOARD_HEIGHT)]
        pygame.init()
        logo = pygame.image.load('assets/logo.png')
        pygame.display.set_icon(logo)
        self.font = pygame.font.Font('assets/fonts/ka1.ttf', size=17)
        self.length_pix: int = BOARD_LENGTH * BLOCK_SIZE + 10*BLOCK_SIZE
        self.height_pix: int = BOARD_HEIGHT*BLOCK_SIZE
        self.display = pygame.display.set_mode((self.length_pix, self.height_pix))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.frame_iteration: int = 0
        self.new_tetromino: Tetromino = self.spawn_tetromino()
        # colors
        self.bg_color = Color.WHITE.value
        self.score_color = Color.BLACK.value
        self.line_separation_color = Color.RED.value
        self.reset()

    def reset(self) -> None:
        self.score = 0
        self.lines_cleared: int = 0
        self.consecutive = 0
        self.game_state = GameState.PLAYING
        self.level = 1
        self.speed = self.level * BASE_SPEED
        self.board = [[None] * BOARD_LENGTH for _ in range(BOARD_HEIGHT)]
        self.frame_iteration = 0
        self.new_tetromino = self.spawn_tetromino()

    def spawn_tetromino(self) -> Tetromino:
        return random_tetromino((int(BOARD_LENGTH/2), 0))

    def update(self, direction, rotate) -> List:
        if self.new_tetromino is None:
            self.new_tetromino = self.spawn_tetromino()
        self.new_tetromino.pos = (self.new_tetromino.pos[0], self.new_tetromino.pos[1]+1)
        if self.collision(self.new_tetromino):
            self.new_tetromino.pos = (self.new_tetromino.pos[0], self.new_tetromino.pos[1]-1)
            self.engrave_to_board(self.new_tetromino)
            self.new_tetromino = self.spawn_tetromino()
            if self.collision(self.new_tetromino):
                self.game_state = GameState.GAME_OVER
        if rotate:
            self.new_tetromino.rotate()
            if self.collision(self.new_tetromino):
                self.new_tetromino.opp_rotate()
        if direction == Direction.RIGHT:
            self.new_tetromino.pos = (self.new_tetromino.pos[0]+1, self.new_tetromino.pos[1])
            if self.collision(self.new_tetromino):
                self.new_tetromino.pos = (self.new_tetromino.pos[0]-1, self.new_tetromino.pos[1])
        if direction == Direction.LEFT:
            self.new_tetromino.pos = (self.new_tetromino.pos[0]-1, self.new_tetromino.pos[1])
            if self.collision(self.new_tetromino):
                self.new_tetromino.pos = (self.new_tetromino.pos[0]+1, self.new_tetromino.pos[1])
        if direction == Direction.DOWN:
            while True:
                self.new_tetromino.pos = (self.new_tetromino.pos[0], self.new_tetromino.pos[1] + 1)
                if self.collision(self.new_tetromino):
                    self.new_tetromino.pos = (self.new_tetromino.pos[0], self.new_tetromino.pos[1] - 1)
                    break
            self.engrave_to_board(self.new_tetromino)
            self.new_tetromino = self.spawn_tetromino()
            if self.collision(self.new_tetromino):
                self.game_state = GameState.GAME_OVER
        score = self.check_board()
        self.level = self.lines_cleared//10 + 1
        self.speed = self.level*BASE_SPEED
        return [score]

    def collision(self, tetromino: Tetromino) -> bool:
        size = len(tetromino.shape)
        x = tetromino.pos[0]
        y = tetromino.pos[1]
        for i in range(size):
            for j in range(size):
                if tetromino.shape[i][j] == 1:
                    if y+j < 0:
                        self.game_state = GameState.GAME_OVER
                        return True
                    if y+j >= BOARD_HEIGHT or x+i < 0 or x+i >= BOARD_LENGTH:
                        return True
                    if self.board[y+j][x+i] is not None:
                        return True
        return False

    def engrave_to_board(self, tetromino):
        size = len(tetromino.shape)
        x = tetromino.pos[0]
        y = tetromino.pos[1]
        for i in range(size):
            for j in range(size):
                if tetromino.shape[i][j] == 1:
                    self.board[y+j][x+i] = tetromino.color

    def check_board(self) -> int:
        """
        Check line clears and award score.
        :return: Score gained
        """
        score = 0
        cleared_lines = []
        for row in range(BOARD_HEIGHT):
            filled = True
            for block in self.board[row]:
                if block is None:
                    filled = False
                    break
            if filled:
                cleared_lines.append(row)
                self.board.pop(row)
                self.board = [[None]*BOARD_LENGTH] + self.board
        count = len(cleared_lines)
        if count > 0:
            self.lines_cleared += count
            score = pow(2, count-1)*100
            score += self.consecutive
            self.score += score
            self.consecutive = self.consecutive*2 + 50
        else:
            self.consecutive = 0
        return score

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
                    self.draw_block(x=BOARD_BORDER_OFFSET + (new_t.pos[0] + i)*BLOCK_SIZE, y=(new_t.pos[1] + j)*BLOCK_SIZE, color=new_t.color)
        # score
        text = self.font.render(f'Level : {self.level}', True, self.score_color)
        self.display.blit(text, ((BOARD_LENGTH+2)*BLOCK_SIZE, int(BLOCK_SIZE/2)))
        text = self.font.render(f'Score', True, self.score_color)
        self.display.blit(text, ((BOARD_LENGTH+2)*BLOCK_SIZE, BLOCK_SIZE*3))
        text = self.font.render(f'{self.score}', True, self.score_color)
        self.display.blit(text, ((BOARD_LENGTH+2)*BLOCK_SIZE, int(BLOCK_SIZE*4)))
        # update the window
        pygame.display.flip()

    def draw_board(self) -> None:
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_LENGTH):
                color = self.board[i][j]
                if color is not None:
                    self.draw_block(x=BOARD_BORDER_OFFSET + j*BLOCK_SIZE, y=i*BLOCK_SIZE, color=color)

    def draw_block(self, x, y, color):
        border_size = 1
        pygame.draw.rect(self.display, Color.BLACK.value, pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, color.value,
                         pygame.Rect(x+border_size, y+border_size, BLOCK_SIZE-border_size*2, BLOCK_SIZE-border_size*2))
