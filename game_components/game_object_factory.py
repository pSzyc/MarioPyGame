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
    __slots__ = ['_x', '_y', '_speed_x', '_speed_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, width: int = 40, height: int = 60, filename: str = 'resources/mario.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._speed_x = int(speed_x)
        self._speed_y = int(speed_y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Mario:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Mario(self._x, self._y, self._speed_x, self._speed_y, ControlMoveStrategy(), image, self._width, self._height)

    
class GhostMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_speed_x', '_speed_y', '_move_strategy', '_mario', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, move_strategy, mario: Mario = None, width: int = 50, height: int = 60, filename: str = 'resources/ghost.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._speed_x = int(speed_x)
        self._speed_y = int(speed_y)
        self._move_strategy = move_strategy
        self._width = int(width)
        self._height = int(height)
        self._mario = mario
        self._filename = filename

    def create(self) -> Ghost:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        image = pygame.transform.flip(image, True, False)
        move_strategy_dispatcher = MoveStrategyDispatcher()
        move_strategy_instance = move_strategy_dispatcher.get_move_strategy(self._move_strategy, self._mario)
        return Ghost(self._x, self._y, self._speed_x, self._speed_y, move_strategy_instance, image, self._width, self._height)

class CoinMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/coin.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Coin:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Coin(self._x, self._y, self._width, self._height, image)
    
class CherryMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/cherry.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Cherry:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Cherry(self._x, self._y, self._width, self._height, image)

class ChestMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int = 60, height: int = 40, filename: str = 'resources/chest.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Chest:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Chest(self._x, self._y, self._width, self._height, image)

class GroundMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int, height: int, texture_width: int = 40, texture_height: int = 40, filename: str = 'resources/ground.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self.texture_width = int(texture_width)
        self.texture_height = int(texture_height)
        width = int(width)
        height = int(height)
        self._width = int(width - (width % self.texture_width))
        self._height = int(height - (height % self.texture_height))
 
        self._filename = filename

    def create(self) -> Ground:
        image = FromFileLoader(self._filename).load_image(self.texture_width, self.texture_height)
        return Ground(self._x, self._y, self._width, self._height, image)

class DoorMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int = 80, height: int = 120, filename: str = 'resources/door.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Door:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Door(self._x, self._y, self._width, self._height, image)

class WineMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, width: int = 40, height: int = 40, filename: str = 'resources/wine.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename

    def create(self) -> Wine:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        return Wine(self._x, self._y, self._width, self._height, image)

class BombMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_speed_x', '_speed_y', '_move_strategy', '_width', '_height', '_filename']
    def __init__(self, x: int, y: int, speed_x: int, speed_y: int, move_strategy: str, width: int = 40, height: int = 40, filename: str = 'resources/bomb.png') -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)
        self._filename = filename
        self._speed_x = int(speed_x)
        self._speed_y = int(speed_y)
        self._move_strategy = move_strategy

    def create(self) -> Bomb:
        image = FromFileLoader(self._filename).load_image(self._width, self._height)
        move_strategy_dispatcher = MoveStrategyDispatcher()
        move_strategy_instance = move_strategy_dispatcher.get_move_strategy(self._move_strategy, None)
        return Bomb(self._x, self._y, self._speed_x, self._speed_y, move_strategy_instance, image, self._width, self._height)

class BoundaryMaker(ObjectMaker):
    __slots__ = ['_x', '_y', '_width', '_height']
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__()
        self._x = int(x)
        self._y = int(y)
        self._width = int(width)
        self._height = int(height)

    def create(self) -> Boundary:
        return Boundary(self._x, self._y, self._width, self._height)

class ObjectFactory():
    __slots__ = ['_makers']
    def __init__(self) -> None:
        self._makers = {
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
        self._makers[type] = maker

    def create(self, type: str, args: tuple) -> GameObject:
        if type in self._makers:
            return self._makers[type](*args).create()
        else:
            raise Exception("Actor type not found.")