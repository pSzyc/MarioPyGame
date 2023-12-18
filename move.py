from abc import ABC, abstractmethod
import pygame

class AbstractMoveStrategy(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def propose_move(self):
        pass


class ControlMoveStrategy(AbstractMoveStrategy):

    def __init__(self):
        super().__init__()

    def propose_move(self, actor):
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            actor.on_turn(isRight = False)
        if keys[pygame.K_RIGHT]:
            actor.on_turn(isRight = True)
        if keys[pygame.K_UP]:
            actor.jump()
        
        x_new = actor.y + actor.speed_y
        y_new = actor.x + actor.speed_x
        
        return x_new, y_new


class BackAndForthMoveStrategy(AbstractMoveStrategy):
    def __init__(self, time_swap = 50):
        super().__init__()
        self.timer = time_swap
        self.time_swap = time_swap

    def propose_move(self, actor):
        self.timer -= 1
        if self.timer == 0:
                self.timer = self.time_swap
                actor.on_turn(isRight = not actor.right)
        
        x_new = actor.y + actor.speed_y
        y_new = actor.x + actor.speed_x

        return x_new, y_new 

class ChaseMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor):
        super().__init__(actor)
    
    def get_move_direction(self):
        pass