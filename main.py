# Example file showing a circle moving on screen
from Grid import Grid
from Snake import Snake
import pygame

# pygame setup
pygame.init()

WIDTH = 900
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0
grid = Grid(10, 10)
num_rows = len(grid.grid)
num_columns = len(grid.grid[0])
rect_width = WIDTH / num_columns
rect_height = HEIGHT / num_rows

MOVE_INTERVAL = 0.07  # Time in seconds between moves
time_since_last_move = 0  # Timer to track time since the last move

snake = Snake()
grid_rect = []
total_collisions = []


# HACER QUE SE HAGA UN SET DE LA SNAKE Y LA MANZANA EN EL GRID. ENTONCES VA A DECIR [SNAKE, BLOCK, APPLE]
# ASI PUEDO ACTUALIZAR Y VER DINAMICAMENTE LOS DATOS EN EL GRID


def draw_grid(): 
    
    for row_index, row in enumerate(grid.grid):
        for col_index, column in enumerate(row):
            outer_rect = pygame.Rect(col_index * rect_width, row_index * rect_height, rect_width, rect_height)
            inner_rect = pygame.Rect(col_index * rect_width + 1, row_index * rect_height + 1, rect_width - 2, rect_height - 2)
            
            grid.get_block(row_index, col_index).rect = [outer_rect, inner_rect]

            grid_rect.append(inner_rect)

            pygame.draw.rect(screen, "black", outer_rect)
            pygame.draw.rect(screen, grid.grid[row_index][col_index].color, inner_rect)

def draw_snake(snake):
    snake_head = pygame.Rect(snake.x_pos, snake.y_pos, rect_width, rect_height)
    pygame.draw.rect(screen, snake.color, snake_head)
    return snake_head

def from_id_to_row_and_col(id):
    row = id//10
    col = id%10
    return row, col

def check_collision(snake_head):
    
    for id, rect in enumerate(grid_rect):
        #print(id, ":" ,rect)
        if rect.colliderect(snake_head):
            block_collided = grid.search_rect_from_block(id,rect)

            print("BLOCK COLLIDED: ", block_collided)
            
            if block_collided is not None and block_collided not in total_collisions:
               # print("Block collided", block_collided)
                block_collided.color = "blue"
                total_collisions.append(block_collided)
        

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    screen.fill("purple")
    draw_grid()
    snake_head = draw_snake(snake)
    check_collision(snake_head)
    grid_rect = []
    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
