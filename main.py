# Example file showing a circle moving on screen
from GamePk.Grid import Grid
from GamePk.Snake import Snake
from GamePk.Player import Player
from GamePk.Screen import Screen
from Game import Game

import pygame
import random
import time
import neat
import os
import pickle


WIDTH = 900
HEIGHT = 900
ROWS = 10
COLUMNS = 10




grid = Grid(ROWS, COLUMNS)
snake = Snake()
player = Player("Porky")
screen = Screen(WIDTH,HEIGHT)
game = Game(screen=screen,grid=grid,player=player,snake=snake )

#game.run_game_human()



def run(config_file, game):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))
    # Run for up to 50 generations.
    winner = p.run(game.run_game_ai, 50000)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))




if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path, game=game)