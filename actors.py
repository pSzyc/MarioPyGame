import numpy as np
from abc import ABC, abstractmethod
import pygame
from move import MoveStrategy
from objects import GameObject

class Actor(GameObject):
    def __init__(self, x, y, speed_x, speed_y, move_strategy, width, height, image):
        super().__init__(x, y, width, height, image)
        self._speed_x = speed_x
        self._speed_y = speed_y
        self._move_strategy = move_strategy

    @property
    def move_strategy(self):
        return self._move_strategy
    
    @move_strategy.setter
    def move_strategy(self, value):
        self._move_strategy = value

    @property
    def speed_x(self):
        return self._speed_x
    
    @speed_x.setter
    def speed_x(self, value):
        self._speed_x = value

    @property
    def speed_y(self):
        return self._speed_y
    
    @speed_y.setter
    def speed_y(self, value):
        self._speed_y = value
    
    def gravity(self, gravity = 1):
        self.speed_y += gravity
    
    @abstractmethod
    def on_turn(self, isRight):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def handle_collision(self, ground):
        pass

class Ghost(Actor):
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, image, width=40, height=40):
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
        self.speed = 2.5
        self.move_strategy = move_strategy
        self.right = True
    
    def on_turn(self, isRight):
        if self.right != isRight:
            self.right = not self.right
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed_x = 2 * (isRight - 0.5) * self.speed

    def handle_collision(self, ground):
        # handle y collision       
        if self.y + self.height / 2 > ground.top and self.y_prev + self.height / 2 <= ground.top:
            self.speed_y = 0
            self.y = ground.top - self.height / 2
        elif self.y - self.height / 2 < ground.bottom and self.y_prev - self.height / 2 >= ground.bottom:
            self.speed_y = 0
            self.y = ground.bottom + self.height / 2

        # handle x collision
        if self.x + self.width / 2 > ground.left and self.x_prev + self.width / 2 <= ground.left:
            self.x = ground.left - self.width / 2
        elif self.x - self.width / 2 < ground.right and self.x_prev - self.width / 2 >= ground.right:
            self.x  = ground.right + self.width / 2

    def move(self):
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class Mario(Actor):
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, image, width=40, height=60):
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
        self.speed = 5
        self.right = True
        self.move_strategy = move_strategy
        self.jump_energy = 0
    
    def on_turn(self, isRight):
        if self.right != isRight:
            self.right = not self.right
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed_x = 2 * (isRight - 0.5) * self.speed
    
    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def jump(self):
        if self.jump_energy >= 10:
            self.speed_y -= self.jump_energy
            self.jump_energy = 0

    def move(self):
        if self.jump_energy < 10:
            self.jump_energy += 0.5
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new
        
    def handle_collision(self, ground):
        # handle y collision       
        if self.y + self.height / 2 > ground.top and self.y_prev + self.height / 2 <= ground.top:
            self.speed_y = 0
            self.jump_energy = 20
            self.y = ground.top - self.height / 2
            self.speed_x -=  0.1 * self.speed_x
        elif self.y - self.height / 2 < ground.bottom and self.y_prev - self.height / 2 >= ground.bottom:
            self.speed_y = 0
            self.y = ground.bottom + self.height / 2
        # handle x collision
        if self.x + self.width / 2 > ground.left and self.x_prev + self.width / 2 <= ground.left:
            self.x = ground.left - self.width / 2
        elif self.x - self.width / 2 < ground.right and self.x_prev - self.width / 2 >= ground.right:
            self.x  = ground.right + self.width / 2