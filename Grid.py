class Block:
    def __init__(self, color, row, column) -> None:
        self.__color = color
        self.__position = (row, column)
        self.__rect = [] #outer_rect - inner_rect
    
    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self,rect) -> list:
        self.__rect = rect

    @property
    def color(self):
        return self.__color
    
    @property
    def position(self):
        return self.__position
    
    @color.setter
    def color(self,color):
        self.__color = color

class Apple(Block):
    def __init__(self, row, column) -> None:
        super().__init__(row, column)
        self.__color = "white"
    


class Grid:
    def __init__(self, rows, columns) -> None:
        self.__rows = rows
        self.__columns = columns
        self.__grid = []
        self.create_grid()

    @property
    def rows(self):
        return self.__rows
    
    @property
    def columns(self):
        return self.__columns
    
    @property
    def grid(self):
        return self.__grid

    def create_grid(self):
        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
                current_block = Block("green", row, column)
                self.grid[row].append(current_block)

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



