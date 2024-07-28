# Example file showing a circle moving on screen
from Game.Grid import Grid
from Game.Snake import Snake
from Game.Player import Player

import pygame
import random
import time
import neat
import os
import pickle

pygame.init()

WIDTH = 900
HEIGHT = 900
ROWS = 10
COLUMNS = 10
STAT_FONT = pygame.font.SysFont("comicsans", 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
grid = Grid(ROWS, COLUMNS)
num_rows = len(grid.grid)
num_columns = len(grid.grid[0])
rect_width = WIDTH / num_columns
rect_height = HEIGHT / num_rows
MOVE_INTERVAL = 0.07  # Time in seconds between moves
time_since_last_move = 0  # Timer to track time since the last move
time_since_last_apple = 0
snake = Snake()
player = Player("Porky")
alive = True

def draw_grid(): 
    for row_index, row in enumerate(grid.grid):
        for col_index, column in enumerate(row):
            outer_rect = pygame.Rect(col_index * rect_width, row_index * rect_height, rect_width, rect_height)
            inner_rect = pygame.Rect(col_index * rect_width + 1, row_index * rect_height + 1, rect_width - 2, rect_height - 2)
            grid.get_block(row_index, col_index).rect = [outer_rect, inner_rect]
            grid.add_to_grid_rect(inner_rect)
            pygame.draw.rect(screen, "black", outer_rect)
            pygame.draw.rect(screen, grid.grid[row_index][col_index].color, inner_rect)

def check_snake_and_apple_collision():
    snake_position = [(snake.y_pos/90), (snake.x_pos/90)]
    if snake_position == grid.apple_position:
        grid.move_apple()
        player.score += 1
        global time_since_last_apple
        time_since_last_apple = 0 

def draw_snake(snake):
    snake_head = pygame.Rect(snake.x_pos, snake.y_pos, rect_width, rect_height)
    pygame.draw.rect(screen, snake.color, snake_head)
    return snake_head

def draw_score():
    score_label = STAT_FONT.render("Score: " + str(player.score),1,(10,25,55))
    screen.blit(score_label, (WIDTH - score_label.get_width() - 15, 10))

def check_bounds(snake):
    if (snake.x_pos > 900 or snake.x_pos < 0) or (snake.y_pos > 900 or snake.y_pos < 0):
        snake.x_pos = 450
        snake.y_pos = 450


def snake_game():
    global dt, time_since_last_move, running, time_since_last_apple


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
                

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                snake.direction = [-1, 0]
            if keys[pygame.K_RIGHT]:
                snake.direction = [1, 0]
            if keys[pygame.K_UP]:
                snake.direction = [0, -1]
            if keys[pygame.K_DOWN]:
                snake.direction = [0, 1]
        

        
        time_since_last_move += dt
        if time_since_last_move >= MOVE_INTERVAL:
            snake.update_position()
            time_since_last_move = 0


        draw_grid()
        draw_score()
        check_bounds(snake)
        snake_head = draw_snake(snake)
        check_snake_and_apple_collision()

        pygame.display.flip()
        dt = clock.tick(60) / 1000

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
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
    winner = p.run(snake_game, 500)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

    with open("best_genome.pickle", "wb") as f:
        pickle.dump(winner, f)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

snake_game()

#if __name__ == '__main__':
#    local_dir = os.path.dirname(__file__)
#    config_path = os.path.join(local_dir, 'config-feedforward.txt')
#    run(config_path)