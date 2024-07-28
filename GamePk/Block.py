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