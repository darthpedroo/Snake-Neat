

class Player:
    def __init__(self, name) -> None:
        self.__name = name
        self.__score = 0

    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, new_score):
        self.__score = new_score

