from GamePk.Block import Block
class Apple(Block):
    def __init__(self, row, column) -> None:
        color = "white"  # Set the default color for Apple
        super().__init__(color, row, column)
        self.__rect = []
        self.__position = (row, column)

    @property
    def rect(self):
        return self.__rect

    @rect.setter
    def rect(self,rect) -> list:
        self.__rect = rect

    @property
    def position(self):
        return self.__position