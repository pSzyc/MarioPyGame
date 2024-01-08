from abc import ABC, abstractmethod
import pygame

class MoveStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def propose_move(self):
        pass

class ControlMoveStrategy(MoveStrategy):
    _instance = None

    def __init__(self) -> None:
        if ControlMoveStrategy._instance is not None:
            raise Exception("Only one instance of ControlMoveStrategy can be created.")
        super().__init__()
        ControlMoveStrategy._instance = self

    @classmethod
    def get_instance(cls) -> 'ControlMoveStrategy':
        if not cls._instance:
            cls._instance = ControlMoveStrategy()
        return cls._instance


    def propose_move(self, actor) -> tuple:
    
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
    def __init__(self, time_swap = 50) -> None:
        super().__init__()
        self.timer = time_swap
        self.time_swap = time_swap

    def propose_move(self, actor) -> tuple:
        self.timer -= 1
        if self.timer == 0:
                self.timer = self.time_swap
                actor.on_turn(isRight = not actor.facing_right)
        x_new = actor.x + actor.speed_x
        y_new = actor.y + actor.speed_y

        return x_new, y_new 

class ChaseMoveStrategy(MoveStrategy):
    def __init__(self, mario) -> None:
        super().__init__()
        self.mario = mario
    
    def propose_move(self, actor) -> tuple:
        x_mario = self.mario.x
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
    def __init__(self) -> None:
        self.dispatch_move_strategy = {
            'control': ControlMoveStrategy,
            'back_and_forth': BackAndForthMoveStrategy,
            'chase': ChaseMoveStrategy
        }
    def register_move_strategy(self, move_strategy_name: str, move_strategy_class: MoveStrategy) -> None:
        self.dispatch_move_strategy[move_strategy_name] = move_strategy_class

    def get_move_strategy(self, move_strategy_name: str, mario = None) -> None:
        move_strategy_class = self.dispatch_move_strategy.get(move_strategy_name)
        if move_strategy_class is None:
            raise ValueError('Invalid move strategy')
        if move_strategy_class == ChaseMoveStrategy:
            if mario is None:
                raise ValueError('Mario must be provided for chase strategy')
            return move_strategy_class(mario)
        else:
            return move_strategy_class()