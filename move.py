from abc import ABC, abstractmethod
import numpy as np

class AbstractMoveStrategy(ABC):
    def __init__(self, actor, board):
        self._actor = actor
        self._board = board
    
    @abstractmethod
    def get_move_direction(self):
        pass

class RandomMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor, board):
        super().__init__(actor, board)
    
    def get_move_direction(self):
        return np.random.choice(['up', 'down', 'left', 'right'])

class ChaseMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor, board):
        super().__init__(actor, board)
    
    def get_move_direction(self):
        packman = self._board.get_packman()
        x, y = packman.x, packman.y
        x_delta = self._actor.x - x
        y_delta = self._actor.y - y

        return 