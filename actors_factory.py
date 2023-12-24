from abc import ABC, abstractmethod
from actors import *
from move import *
from graphics import *
from objects import *
from ground import *

class ObjectMaker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass

class MarioMaker(ObjectMaker):
    def __init__(self, x, y, speed_x, speed_y, width, height, filename = 'resources/mario.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.speed_x = int(speed_x)
        self.speed_y = int(speed_y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Mario(self.x, self.y, self.speed_x, self.speed_y, ControlMoveStrategy(), image, self.width, self.height)

    
class GhostMaker(ObjectMaker):
    def __init__(self, x, y, speed_x, speed_y, move_strategy, width, height, mario = None, filename = 'resources/mario_ghost.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.speed_x = int(speed_x)
        self.speed_y = int(speed_y)
        self.move_strategy = move_strategy
        self.width = int(width)
        self.height = int(height)
        self.mario = mario
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        move_strategy_instance = get_move_strategy(self.move_strategy, self.mario)
        return Ghost(self.x, self.y, self.speed_x, self.speed_y, move_strategy_instance, image, self.width, self.height)

class CoinMaker(ObjectMaker):
    def __init__(self, x, y, width, height, filename = 'resources/coin.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Coin(self.x, self.y, self.width, self.height, image)
    
class CherryMaker(ObjectMaker):
    def __init__(self, x, y, width, height, filename = 'resources/cherry.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Cherry(self.x, self.y, self.width, self.height, image)

class ChestMaker(ObjectMaker):
    def __init__(self, x, y, width, height, filename = 'resources/chest.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Chest(self.x, self.y, self.width, self.height, image)

class GroundMaker(ObjectMaker):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    def create(self):
        return Ground(self.x, self.y, self.width, self.height)


class ObjectFactory():
    def create(self, type, args):
        if type == Mario.__name__:
            return MarioMaker(*args).create()
        elif type == Ghost.__name__:
            return GhostMaker(*args).create()
        elif type == Coin.__name__:
            return CoinMaker(*args).create()
        elif type == Cherry.__name__:
            return CherryMaker(*args).create()
        elif type == Chest.__name__:
            return ChestMaker(*args).create()
        elif type == Ground.__name__:
            return GroundMaker(*args).create()
        else:
            raise Exception("Actor type not found.")