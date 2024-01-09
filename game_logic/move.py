from abc import ABC, abstractmethod
import sys
sys.path.append('..')
import pygame

class MoveStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def propose_move(self) -> tuple[int, int]:
        pass

class ControlMoveStrategy(MoveStrategy):
    _instance = None

    def __init__(self) -> None:
        if ControlMoveStrategy._instance is not None:
            raise Exception("Only one instance of ControlMoveStrategy can be created.")
        super().__init__()
        ControlMoveStrategy._instance = self

    def propose_move(self, actor: 'Actor') -> tuple[int, int]:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            actor.on_turn(isRight = False)
        if keys[pygame.K_RIGHT]:
            actor.on_turn(isRight = True)
        if keys[pygame.K_UP]:
            actor.jump()
        
        x_new = actor.x + actor.speed_x
        y_new = actor.y + actor.speed_y
        
        return x_new, y_new


class BackAndForthMoveStrategy(MoveStrategy):

    __slots__ = ['_timer', '_time_swap']
    def __init__(self, time_swap = 50) -> None:
        super().__init__()
        self._timer = time_swap
        self._time_swap = time_swap

    def propose_move(self, actor: 'Actor') -> tuple[int, int]:
        self._timer -= 1
        if self._timer == 0:
                self._timer = self._time_swap
                actor.on_turn(isRight = not actor.facing_right)
        x_new = actor.x + actor.speed_x
        y_new = actor.y + actor.speed_y

        return x_new, y_new 

class ChaseMoveStrategy(MoveStrategy):

    __slots__ = ['_mario']
    def __init__(self, mario: 'Mario') -> None:
        super().__init__()
        self._mario = mario
    
    def propose_move(self, actor) -> tuple[int, int]:
        x_mario = self._mario.x
        x_actor = actor.x
        if abs(x_mario - x_actor) < 300:
            if x_mario < x_actor:
                actor.on_turn(isRight = False)
            else:  
                actor.on_turn(isRight = True)
            x_new = actor.x + actor.speed_x
        else:
            x_new = actor.x
        
        y_new = actor.y + actor.speed_y
        return x_new, y_new

class MoveStrategyDispatcher:
    
    __slots__ = ['_dispatch_move_strategy']
    def __init__(self) -> None:
        self._dispatch_move_strategy = {
            'control': ControlMoveStrategy,
            'back_and_forth': BackAndForthMoveStrategy,
            'chase': ChaseMoveStrategy
        }
    def register_move_strategy(self, move_strategy_name: str, move_strategy_class: MoveStrategy) -> None:
        self._dispatch_move_strategy[move_strategy_name] = move_strategy_class

    def get_move_strategy(self, move_strategy_name: str, mario: 'Mario' = None) -> None:
        move_strategy_class = self._dispatch_move_strategy.get(move_strategy_name)
        if move_strategy_class is None:
            raise ValueError('Invalid move strategy')
        if move_strategy_class == ChaseMoveStrategy:
            if mario is None:
                raise ValueError('Mario must be provided for chase strategy')
            return move_strategy_class(mario)
        else:
            return move_strategy_class()