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
    def create(self) -> GameObject:
        pass

class MarioMaker(ObjectMaker):
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, width: int = 40, height: int = 60, filename: str = 'resources/mario.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.speed_x = int(speed_x)
        self.speed_y = int(speed_y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Mario:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Mario(self.x, self.y, self.speed_x, self.speed_y, ControlMoveStrategy(), image, self.width, self.height)

    
class GhostMaker(ObjectMaker):
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, move_strategy, mario: Mario = None, width: int = 50, height: int = 60, filename: str = 'resources/ghost.png') -> None:
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

    def create(self) -> Ghost:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        image = pygame.transform.flip(image, True, False)
        move_strategy_dispatcher = MoveStrategyDispatcher()
        move_strategy_instance = move_strategy_dispatcher.get_move_strategy(self.move_strategy, self.mario)
        return Ghost(self.x, self.y, self.speed_x, self.speed_y, move_strategy_instance, image, self.width, self.height)

class CoinMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/coin.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Coin:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Coin(self.x, self.y, self.width, self.height, image)
    
class CherryMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/cherry.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Cherry:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Cherry(self.x, self.y, self.width, self.height, image)

class ChestMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int = 60, height: int = 40, filename: str = 'resources/chest.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Chest:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Chest(self.x, self.y, self.width, self.height, image)

class GroundMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int, height: int, texture_width: int = 40, texture_height: int = 40, filename: str = 'resources/ground.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.texture_width = int(texture_width)
        self.texture_height = int(texture_height)
        width = int(width)
        height = int(height)
        self.width = int(width - (width % self.texture_width))
        self.height = int(height - (height % self.texture_height))
 
        self.filename = filename

    def create(self) -> Ground:
        image = FromFileLoader(self.filename).load_image(self.texture_width, self.texture_height)
        return Ground(self.x, self.y, self.width, self.height, image)

class DoorMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int = 80, height: int = 120, filename: str = 'resources/door.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Door:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Door(self.x, self.y, self.width, self.height, image)

class WineMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/wine.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename

    def create(self) -> Wine:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        return Wine(self.x, self.y, self.width, self.height, image)

class BombMaker(ObjectMaker):
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, move_strategy: str, width: int = 40, height: int = 40, filename: str = 'resources/bomb.png') -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.filename = filename
        self.speed_x = int(speed_x)
        self.speed_y = int(speed_y)
        self.move_strategy = move_strategy

    def create(self) -> Bomb:
        image = FromFileLoader(self.filename).load_image(self.width, self.height)
        move_strategy_dispatcher = MoveStrategyDispatcher()
        move_strategy_instance = move_strategy_dispatcher.get_move_strategy(self.move_strategy, None)
        return Bomb(self.x, self.y, self.speed_x, self.speed_y, move_strategy_instance, image, self.width, self.height)

class BoundaryMaker(ObjectMaker):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__()
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)

    def create(self) -> Boundary:
        return Boundary(self.x, self.y, self.width, self.height)

class ObjectFactory():
    def __init__(self) -> None:
        self.makers = {
            Mario.__name__: MarioMaker,
            Ghost.__name__: GhostMaker,
            Coin.__name__: CoinMaker,
            Cherry.__name__: CherryMaker,
            Chest.__name__: ChestMaker,
            Ground.__name__: GroundMaker,
            Door.__name__: DoorMaker,
            Boundary.__name__: BoundaryMaker,
            Wine.__name__: WineMaker,
            Bomb.__name__: BombMaker
        }

    def register(self, type: str, maker: ObjectMaker) -> None:
        self.makers[type] = maker

    def create(self, type: str, args: tuple) -> GameObject:
        if type in self.makers:
            return self.makers[type](*args).create()
        else:
            raise Exception("Actor type not found.")