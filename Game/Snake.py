import random
class Snake:
    def __init__(self):
        self.__x_pos = 450
        self.__y_pos = 450
        self.__vel = 90
        self.__direction = [0,0]
        self.__color = "red"

    @property
    def color(self):
        return self.__color

    @property
    def direction(self):
        return self.__direction

    @direction.setter
    def direction(self, new_direction) -> list:
        self.__direction = new_direction

    @property
    def vel(self):
        return self.__vel   
    
    @property
    def x_pos(self):
        return self.__x_pos

    @x_pos.setter
    def x_pos(self, new_x_position):
        self.__x_pos = new_x_position

    @property
    def y_pos(self):
        return self.__y_pos

    @y_pos.setter
    def y_pos(self, new_y_position):
        self.__y_pos = new_y_position

    def update_position(self):
       self.x_pos += self.direction[0]*self.vel
       self.y_pos += self.direction[1]*self.vel

    

    

    
    