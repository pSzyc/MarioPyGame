from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from game_components.actors import *
from game_logic.move import *
from utilities.graphics import *
from game_components.game_objects import *

class ObjectMaker(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create(self):
        pass

class MarioMaker(ObjectMaker):
    def __init__(self, x, y, speed_x, speed_y, width = 40, height = 60, filename = 'resources/mario.png'):
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
    def __init__(self, x, y, speed_x, speed_y, move_strategy, mario = None, width= 50, height = 60, filename = 'resources/ghost.png'):
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
        image = pygame.transform.flip(image, True, False)
        move_strategy_instance = get_move_strategy(self.move_strategy, self.mario)
        return Ghost(self.x, self.y, self.speed_x, self.speed_y, move_strategy_instance, image, self.width, self.height)

class CoinMaker(ObjectMaker):
    def __init__(self, x, y, width = 40, height = 40, filename = 'resources/coin.png'):
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
    def __init__(self, x, y, width = 40, height = 40, filename = 'resources/cherry.png'):
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
    def __init__(self, x, y, width = 60, height = 40, filename = 'resources/chest.png'):
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
    def __init__(self, x, y, width, height, texture_width = 40, texture_height = 40, filename = 'resources/ground.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.texture_width = int(texture_width)
        self.texture_height = int(texture_height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.texture_width, self.texture_height)
        return Ground(self.x, self.y, self.width, self.height, image)

class DoorMaker(ObjectMaker):
    def __init__(self, x, y, width = 80, height = 120, filename = 'resources/door.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Door(self.x, self.y, self.width, self.height, image)

class BoundaryMaker(ObjectMaker):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    def create(self):
        return Boundary(self.x, self.y, self.width, self.height)

class WineMaker(ObjectMaker):
    def __init__(self, x, y, width = 40, height = 40, filename = 'resources/wine.png'):
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self):
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Wine(self.x, self.y, self.width, self.height, image)

class ObjectFactory():
        def __init__(self):
            self.makers = {
                Mario.__name__: MarioMaker,
                Ghost.__name__: GhostMaker,
                Coin.__name__: CoinMaker,
                Cherry.__name__: CherryMaker,
                Chest.__name__: ChestMaker,
                Ground.__name__: GroundMaker,
                Door.__name__: DoorMaker,
                Boundary.__name__: BoundaryMaker,
                Wine.__name__: WineMaker
            }

        def register(self, type, maker):
            self.makers[type] = maker

        def create(self, type, args):
            if type in self.makers:
                return self.makers[type](*args).create()
            else:
                raise Exception("Actor type not found.")
