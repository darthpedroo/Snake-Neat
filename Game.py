import pygame
        

class Game:
    pygame.init()
    MOVE_INTERVAL = 0.07
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

    def draw_grid(self):
        for row_index, row in enumerate(self.grid.grid):
            for col_index, column in enumerate(row):
                outer_rect = pygame.Rect(col_index * self.rect_width, row_index * self.rect_height, self.rect_width, self.rect_height)
                inner_rect = pygame.Rect(col_index * self.rect_width + 1, row_index * self.rect_height + 1, self.rect_width - 2, self.rect_height - 2)
                self.grid.get_block(row_index, col_index).rect = [outer_rect, inner_rect]
                self.grid.add_to_grid_rect(inner_rect)
                pygame.draw.rect(self.screen.screen, "black", outer_rect)
                pygame.draw.rect(self.screen.screen, self.grid.grid[row_index][col_index].color, inner_rect)

    def check_snake_and_apple_collision(self):
        if self.snake.position == self.grid.apple_position:
            self.grid.move_apple()
            self.player.score += 1
            self.__time_since_last_apple = 0
    
    def draw_snake(self):
        snake_head = pygame.Rect(self.snake.x_pos, self.snake.y_pos, self.rect_width, self.rect_height)
        pygame.draw.rect(self.screen.screen, self.snake.color, snake_head)
        return snake_head
    
    def draw_score(self):
        score_label = self.STAT_FONT.render("Score: " + str(self.player.score),1,(10,25,55))
        self.screen.screen.blit(score_label, (self.screen.width - score_label.get_width() - 15, 10))
    
    def check_bounds(self):
        if (self.snake.x_pos > 900 or self.snake.x_pos < 0) or (self.snake.y_pos > 900 or self.snake.y_pos < 0):
            self.snake.x_pos = 450
            self.snake.y_pos = 450
            self.player.score = 0
            self.snake.direction = [0,0]

    def run_game(self):
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
            self.check_bounds()
            snake_head = self.draw_snake()
            self.check_snake_and_apple_collision()
            pygame.display.flip()
            self.dt = self.clock.tick(60) / 1000



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
        

