from abc import ABC, abstractmethod
from actors import *
from move import *
from graphics import *


class ActorMaker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_actor(self):
        pass

class MarioMaker(ActorMaker):
    def __init__(self):
        super().__init__()

    def create_actor(self, x, y, speed_x, speed_y, width, height, filename = 'mario.webp'):
        image = FromFileLoader(filename).load_image(width, height)
        return Mario(x, y, speed_x, speed_y, ControlMoveStrategy(), image, width, height)

    
class GhostMaker(ActorMaker):
    def __init__(self):
        super().__init__()

    def create_actor(self, x, y, speed_x, speed_y, move_strategy, width, height, mario = None, filename = 'mario_ghost.png'):
        image = FromFileLoader(filename).load_image(width, height)
        move_strategy_instance = get_move_strategy(move_strategy, mario)
        return Ghost(x, y, speed_x, speed_y, move_strategy_instance, image, width, height)

