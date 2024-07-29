import pygame
import neat
import time
from GamePk.Snake import Snake

class Game:
    pygame.init()
    MOVE_INTERVAL = 0.05
    MAX_TIME_TO_CATCH_APPLE = 3
    STAT_FONT = pygame.font.SysFont("comicsans", 50)
    def __init__(self, screen, grid, player,snake) -> None:
        self.__screen = screen
        self.__grid = grid
        self.__player = player
        self.__snake = snake
        self.__clock = self.create_clock()
        self.__running = True
        self.__dt = 0
        self.__time_since_last_move = 0
        self.__time_since_last_apple = 0
        self.__rect_width = 90
        self.__rect_height = 90
        self.__current_snake = 0
        self.__snakes = []
        self.__ge = []
        self.__distance_to_apple = []



    def draw_grid(self):
        for row_index, row in enumerate(self.grid.grid):
            for col_index, column in enumerate(row):
                outer_rect = pygame.Rect(col_index * self.rect_width, row_index * self.rect_height, self.rect_width, self.rect_height)
                inner_rect = pygame.Rect(col_index * self.rect_width + 1, row_index * self.rect_height + 1, self.rect_width - 2, self.rect_height - 2)
                self.grid.get_block(row_index, col_index).rect = [outer_rect, inner_rect]
                self.grid.add_to_grid_rect(inner_rect)
                pygame.draw.rect(self.screen.screen, "black", outer_rect)
                pygame.draw.rect(self.screen.screen, self.grid.grid[row_index][col_index].color, inner_rect)

    def check_snake_and_apple_collision(self, genome):
        if self.snake.position == self.grid.apple_position:
            self.grid.move_apple()
            self.player.score += 1
            self.__time_since_last_apple = 0
            genome.fitness += 100
    
    def draw_snake(self):
        snake_head = pygame.Rect(self.snake.x_pos, self.snake.y_pos, self.rect_width, self.rect_height)
        pygame.draw.rect(self.screen.screen, self.snake.color, snake_head)
        return snake_head
    
    def draw_score(self):
        score_label = self.STAT_FONT.render("Score: " + str(self.player.score),1,(10,25,55))
        genome_fitness_label = self.STAT_FONT.render("FIT: " + str(self.ge[self.current_snake-1].fitness),1,(10,25,55)) 
        time_since_last_apple_label = self.STAT_FONT.render("time: " + str(self.time_since_last_apple),1,(10,25,55))

        
        self.screen.screen.blit(score_label, (self.screen.width - score_label.get_width() - 15, 10))
        self.screen.screen.blit(genome_fitness_label, (self.screen.width - score_label.get_width() - 50, 100))
        self.screen.screen.blit(time_since_last_apple_label, (self.screen.width - score_label.get_width() - 100, 150))
    
    def check_bounds(self,genome):
        if (self.snake.x_pos > 900 or self.snake.x_pos < 0) or (self.snake.y_pos > 900 or self.snake.y_pos < 0):
            self.player.score = 0
            self.current_snake += 1
            self.time_since_last_apple = 0
            self.snake = self.snakes[self.current_snake]
            self.snake.x_pos = 450
            self.snake.y_pos = 450            
            self.snake.direction = [0,0]  
            genome.fitness -= 50

    def kill_after_5_seconds(self,genome):
        if self.time_since_last_apple > self.MAX_TIME_TO_CATCH_APPLE:
            self.time_since_last_apple = 0
            self.current_snake += 1
            genome.fitness -= 200

    def check_distance_to_apple(self):
            distance = [abs(self.grid.apple_position[0] - self.snake.position[0]), abs(self.grid.apple_position[1] - self.snake.position[1])]
            return distance

    def change_fitness(self, genome, points):
        genome.fitness += points

    def check_if_near_to_wall(self,genome):
        if abs(self.snake.position[0] - 9) == 0 or abs(self.snake.position[0]) == 0 :
            self.change_fitness(genome, -10)
        
        if abs(self.snake.position[1] - 9) == 0 or abs(self.snake.position[1]) == 0 :
            self.change_fitness(genome, -10)
        

    def check_if_staying_in_place():
        pass

    def run_game_human(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.snake.direction = [-1, 0]
            if keys[pygame.K_RIGHT]:
                self.snake.direction = [1, 0]
            if keys[pygame.K_UP]:
                self.snake.direction = [0, -1]
            if keys[pygame.K_DOWN]:
                self.snake.direction = [0, 1]

            self.time_since_last_move += self.dt
            if self.time_since_last_move >= self.MOVE_INTERVAL:
                self.snake.update_position()
                self.time_since_last_move = 0
            
            self.draw_grid()
            self.draw_score()
            self.check_bounds(1)
            snake_head = self.draw_snake()
            self.check_snake_and_apple_collision(1)
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000

    def run_game_ai(self, genomes, config):

        #time.sleep(1)
        print("SNAKES: ", self.snakes)
        
        self.current_snake = 0
        self.running = True
        self.time_since_last_apple = 0
        self.time_since_last_move = 0 
        self.snakes = []
        self.ge = []
        self.dt = 0
    
      

        nets = []
        


        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            self.snakes.append(Snake())
            self.ge.append(genome)
        
        self.snakes[self.current_snake].x_pos = 450
        self.snakes[self.current_snake].y_pos = 450

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    quit()
        

            try:
                output = nets[self.current_snake].activate(
                    (
                    int(self.snakes[self.current_snake].position[0]),
                    int(self.snakes[self.current_snake].position[1]), 
                    int(self.grid.apple_position[0]),
                    int(self.grid.apple_position[1]),
                    abs(self.snake.position[0] - 9),
                    abs(self.snake.position[1] - 9),
                    )
                )
                move = output.index(max(output))
                #print(move)

                if move == 0:
                    self.snake.direction = [-1, 0]
                if move == 1:
                    self.snake.direction = [1, 0]
                if move == 2:
                    self.snake.direction = [0, -1]
                if move == 3:
                    self.snake.direction = [0, 1]

                self.time_since_last_move += self.dt
                self.time_since_last_apple += self.dt
                if self.time_since_last_move >= self.MOVE_INTERVAL:

                    distance_before_move = self.check_distance_to_apple()
                    
                    self.snake.update_position()
                    
                    distanace_after_move = self.check_distance_to_apple()

                    
                    if distanace_after_move[0] > distance_before_move[0]:
                        pass
                       # self.ge[self.current_snake].fitness -= 20
                    elif distanace_after_move[0] < distance_before_move[0]:
                        print("skibi")
                        print(distanace_after_move[0] - distance_before_move[0]) 
                        pass
                   #     self.ge[self.current_snake].fitness += 50
                    elif distanace_after_move[1] > distance_before_move[1]:
                        pass
                     #   self.ge[self.current_snake].fitness -= 20
                    elif distanace_after_move[1] < distance_before_move[1]:
                        pass
                    #    self.ge[self.current_snake].fitness += 50
                    
                    self.check_if_near_to_wall(self.ge[self.current_snake])

                    self.time_since_last_move = 0
                
                self.draw_grid()
                self.draw_score()
                self.check_bounds(self.ge[self.current_snake])
                snake_head = self.draw_snake()
                
                self.check_snake_and_apple_collision(self.ge[self.current_snake])
                self.kill_after_5_seconds(self.ge[self.current_snake])
                pygame.display.flip()
                self.dt = self.clock.tick(60) / 1000
            except:
                Exception(OverflowError)
                self.running = False

            






    @property
    def clock(self):
        return self.__clock

    @property
    def dt(self):
        return self.__dt
    
    @dt.setter
    def dt(self, new_dt):
        self.__dt = new_dt
    
    @property
    def time_since_last_move(self):
        return self.__time_since_last_move
    
    @time_since_last_move.setter
    def time_since_last_move(self, new_time):
        self.__time_since_last_move = new_time

    @property
    def time_since_last_apple(self):
        return self.__time_since_last_apple
    
    @time_since_last_apple.setter
    def time_since_last_apple(self, new_time):
        self.__time_since_last_apple = new_time

    @property
    def player(self):
        return self.__player
    
    @property
    def snake(self):
        return self.__snake
    
    @snake.setter
    def snake(self, new_snake):
        self.__snake = new_snake

    @property
    def screen(self):
        return self.__screen
    
    @property
    def grid(self):
        return self.__grid
    
    @property
    def rect_width(self):
        return self.__rect_width
    
    @property
    def rect_height(self):
        return self.__rect_height

    @property
    def running(self):
        return self.__running

    @running.setter
    def running(self, new_value):
        self.__running = new_value

    def create_clock(self):
        return pygame.time.Clock()

    @property
    def distance_to_apple(self):
        return self.__distance_to_apple
    
    @distance_to_apple.setter
    def distance_to_apple(self, new_distance):
        self.__distance_to_apple = new_distance


    @property
    def snakes(self):
        return self.__snakes
    
    @snakes.setter
    def snakes(self, new_snakes):
        self.__snakes = new_snakes
    
    @property
    def ge(self):
        return self.__ge

    @ge.setter
    def ge(self, new_ge):
        self.__ge = new_ge

    @property
    def current_snake(self):
        return self.__current_snake
    
    @current_snake.setter
    def current_snake(self, new_snake_idx):
        self.__current_snake = new_snake_idx


