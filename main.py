import argparse
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
from tetris import Tetris
from constants import *

parser = argparse.ArgumentParser("arg_parser")
parser.add_argument("-player", help="Values = 'AI'(Default) or 'USER'", type=str)


if __name__ == "__main__":
    args = parser.parse_args()
    player = args.player or AI
    if player not in VALID_PLAYERS:
        raise ValueError(f"player flags needs to be one of {VALID_PLAYERS}")
    print(f"Player: {player}")

    game = Tetris()
    # pygame loop
    while game.game_state != GameState.GAME_OVER:
        direction = None
        rotate = False
        game.frame_iteration += 1
        # get inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print(f"Quit Event: Quitting Game.")
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    direction = Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    direction = Direction.DOWN
                elif event.key == pygame.K_UP:
                    rotate = True
        game.update(direction, rotate)
        # update UI
        game.update_ui()
        # frame rate
        game.clock.tick(SPEED)
    input(f"Game Over!")
