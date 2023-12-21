from abc import ABC, abstractmethod
from actors import *
from move import *
from graphics import *
from objects import *

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

class CoinMaker(ActorMaker):
    def __init__(self):
        super().__init__()

    def create_actor(self, x, y, width, height, filename = 'coin.png'):
        image = FromFileLoader(filename).load_image(width, height)
        return Coin(x, y, width, height, image)
    
class CherryMaker(ActorMaker):
    def __init__(self):
        super().__init__()

    def create_actor(self, x, y, width, height, filename = 'cherry.png'):
        image = FromFileLoader(filename).load_image(width, height)
        return Cherry(x, y, width, height, image)
    
class ChestMaker(ActorMaker):
    def __init__(self):
        super().__init__()

    def create_actor(self, x, y, width, height, filename = 'chest.png'):
        image = FromFileLoader(filename).load_image(width, height)
        return Chest(x, y, width, height, image)
