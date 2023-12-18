from abc import ABC, abstractmethod
import pygame
class AbstractMoveStrategy(ABC):
    def __init__(self, actor):
        self._actor = actor
    
    @property
    def actor(self):
        return self._actor

    @abstractmethod
    def make_move(self):
        pass


class ControlMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor):
        super().__init__(actor)

    def make_move(self):
        if self.actor.jump_energy < 10:
            self.actor.jump_energy += 0.5

        self.actor.x_prev = self.actor.x
        self.actor.y_prev = self.actor.y
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.actor.speed_x = -5
            self.actor.on_turn(isRight = False)

        if keys[pygame.K_RIGHT]:
            self.actor.speed_x = 5
            self.actor.on_turn(isRight = True)
                
        if keys[pygame.K_UP]:
            if self.actor.jump_energy >= 10:
                self.actor.speed_y -= self.actor.jump_energy
                self.actor.jump_energy = 0
        
        self.actor.y += self.actor.speed_y
        self.actor.x += self.actor.speed_x

    def gravity(self):
        self.actor.speed_y += 1


class BackAndForthMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor, time_swap = 50, swap_axis = 'x'):
        super().__init__(actor)
        self._direction = 1
        self.timer = time_swap
        self.time_swap = time_swap
        self.swap_axis = swap_axis

    def make_move(self):
        self.timer -= 1
        if self.timer == 0:
                self.timer = self.time_swap
                if self.swap_axis == 'x':
                    self.actor.speed_x *= -1
                else:
                    self.actor.speed_y *= -1
                self.actor.on_turn(isRight = not self.actor.right)
        self.actor.x_prev = self.actor.x
        self.actor.y_prev = self.actor.y
        self.actor.x += self.actor.speed_x
        self.actor.y += self.actor.speed_y        
class ChaseMoveStrategy(AbstractMoveStrategy):
    def __init__(self, actor):
        super().__init__(actor)
    
    def get_move_direction(self):
        pass