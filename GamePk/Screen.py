import pygame

class Screen:
    def __init__(self, width, height) -> None:
        self.__width = width
        self.__height = height
        self.__screen = self.create_screen()

    @property
    def screen(self):
        return self.__screen

    @property
    def width(self):
        return self.__width
    
    @property
    def height(self):
        return self.__height

    def create_screen(self):
        return pygame.display.set_mode((self.width, self.height))