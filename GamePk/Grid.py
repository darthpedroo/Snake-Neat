import random
from GamePk.Block import Block
from GamePk.Apple import Apple

class Grid:
    BACKGROUND_COLOR = "GREEN"
    def __init__(self, rows, columns) -> None:
        self.__rows = rows
        self.__columns = columns
        self.__grid = []
        self.__grid_rect = []
        self.__apple_position = []
        self.create_grid()


    def add_to_grid_rect(self, inner_rect):
        self.__grid_rect.append(inner_rect)

    def set_block(self,position ,block_class):
        self.__grid[position[0]][position[1]] = block_class

    @property
    def apple_position(self):
        return self.__apple_position

    @apple_position.setter
    def apple_position(self, position) -> list:
        self.__apple_position = position

    @property
    def grid_rect(self):
        return self.__grid_rect

    @property
    def rows(self):
        return self.__rows
    
    @property
    def columns(self):
        return self.__columns
    
    @property
    def grid(self):
        return self.__grid
    
    def move_apple(self):
        block = Block(self.BACKGROUND_COLOR,self.apple_position[0],self.apple_position[1])
        self.set_block(self.apple_position, block)
        x = random.randint(0,9)
        y = random.randint(0,9)
        pos = [x,y]
        apple = Apple(x ,y)
        self.apple_position = pos
        self.set_block(self.apple_position, apple)


        pass

    def create_grid(self):
        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
                current_block = Block("green", row, column)
                self.grid[row].append(current_block)
        x = random.randint(0,9)
        y = random.randint(0,9)
        pos = [x,y]
        apple = Apple(x ,y)
        self.apple_position = pos
        self.set_block(apple.position,apple)
        

    def search_block(self,row,column):
        return self.grid[row][column]
    
    def search_rect_from_block(self,id,rect):
        row = id//10
        col = id%10
        try:
            x = self.grid[row][col]
            print("AT: ", row, col)
            return (x)
        except:
            print(row)
            print(col)

    def get_block(self, row_index, col_index):
        return self.grid[row_index][col_index]



