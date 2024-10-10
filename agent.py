import random
from collections import deque
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import numpy
import numpy as np
from utils import plot
from ai import QModel, QTrainer
from constants import GameState, MAX_MEMORY, BATCH_SIZE, Direction, BOARD_HEIGHT
from tetris import Tetris


class Agent:
    def __init__(self, epsilon: float = None):
        self.game: Tetris = Tetris()
        self.input_dim: int = len(self.get_state(self.game))
        self.output_dim: int = 4
        self.model: QModel = QModel(self.input_dim, [512], self.output_dim)
        self.trainer: QTrainer = QTrainer(self.model)
        self.memory = deque(maxlen=MAX_MEMORY)
        self.epsilon: float = epsilon

    @staticmethod
    def get_state(game) -> numpy.ndarray:
        """
        Extracts the state of game in format that is accepted by model.
        :param game:
        :return:
        """
        state = []
        # current new tetromino
        state.extend(game.new_tetromino.pos)
        state.extend(sum(game.new_tetromino.shape, []))
        # board
        state.extend(sum([[0 if block is None else 1 for block in row] for row in game.board], []))
        return np.array(state, dtype=int)

    @staticmethod
    def penalties(game, score):
        """
        Additional penalties imposed.
        1. Penalize for high structures
        :param score:
        :param game:
        :return:
        """
        blocks = 0
        non_blocks = 0
        highest_row = BOARD_HEIGHT-1
        for i in range(BOARD_HEIGHT):
            for block in game.board[i]:
                if block is not None:
                    highest_row = i
                    break
            if highest_row != BOARD_HEIGHT-1:
                break
        # only penalize if not scored
        if score <= 0 and game.new_tetromino.pos[0] <= 1:
            score += -(BOARD_HEIGHT-highest_row)
        return score

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_term_memory(self):
        """
        Memory Relay Concept
        :return:
        """
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = random.sample(self.memory, len(self.memory))
        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_term_memory(self, state_old, move, reward, state_new, game_over):
        self.trainer.train_step(state_old, move, reward, state_new, game_over)

    def train(self):
        """
        Trains self.model
        :return:
        """
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        highest_score = 0
        n_games = 0
        while True:
            # get old state
            state_old = self.get_state(self.game)
            # get move
            epsilon = (150-n_games)/350
            if n_games > 150 and self.epsilon is not None:
                epsilon = self.epsilon
            move = self.model.get_move(state_old, epsilon)
            rotate = False
            direction = None
            if move[Direction.RIGHT.value] == 1:
                direction = Direction.RIGHT
            elif move[Direction.DOWN.value] == 1:
                direction = Direction.DOWN
            elif move[Direction.LEFT.value] == 1:
                direction = Direction.LEFT
            else:
                rotate = True
            rewards = self.game.update(direction, rotate)
            self.game.update_ui()
            # frame rate
            speed = 100
            self.game.clock.tick(speed)
            score = rewards[0]
            score = self.penalties(self.game, score)
            state_new = self.get_state(self.game)
            game_over = self.game.game_state == GameState.GAME_OVER
            # train short term memory
            self.train_short_term_memory(state_old, move, score, state_new, game_over)
            # remember
            self.remember(state_old, move, score, state_new, game_over)
            # if game-over then memory-replay
            if game_over:
                self.game.reset()
                n_games += 1
                self.train_long_term_memory()
                if score > highest_score:
                    highest_score = score
                    self.model.save()
                print(f'Game:{n_games}\t Epsilon: {epsilon} Score:{score}\t Highest:{highest_score}')
                # plot
                plot_scores.append(score)
                total_score += score
                mean_score = total_score/n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    print(f"Quit Event: Quitting Game.")
                    exit()


a = Agent()
a.train()
