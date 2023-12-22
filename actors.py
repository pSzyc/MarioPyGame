import numpy as np
from abc import ABC, abstractmethod
import pygame
from move import MoveStrategy
from objects import GameObject

class Actor(GameObject):
    def __init__(self, x, y, speed_x, speed_y, move_strategy, collision_handler, width, height, image):
        super().__init__(x, y, width, height, image)
        self._speed_x = speed_x
        self._speed_y = speed_y
        self.x_prev = x
        self.y_prev = y
        self._move_strategy = move_strategy
        self._collision_handler = collision_handler

    @property
    def collision_handler(self):
        return self._collision_handler
    
    @collision_handler.setter
    def collision_handler(self, collision_handler):
        self._collision_handler = collision_handler
    
    @property
    def prev_rectangle(self):
        return pygame.Rect(self.x_prev - self.width / 2, self.y_prev - self.height / 2, self.width, self.height)

    @property
    def move_strategy(self):
        return self._move_strategy
    
    @move_strategy.setter
    def move_strategy(self, move_strategy):
        self._move_strategy = move_strategy

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
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, collision_handler, image, width=40, height=40):
        super().__init__(x, y, speed_x, speed_y, move_strategy, collision_handler, width, height, image)
        self.speed = 2.5
        self.right = True
    
    def on_turn(self, isRight):
        if self.right != isRight:
            self.right = not self.right
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed_x = 2 * (isRight - 0.5) * self.speed

    def handle_collision(self, ground):
        self.collision_handler.handle_collision(self, ground)

    def move(self):
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class Mario(Actor):
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, collision_handler, image, width=40, height=60):
        super().__init__(x, y, speed_x, speed_y, move_strategy, collision_handler, width, height, image)
        self.speed = 5
        self.right = True
        self.jump_energy = 0
        self.lifes = 3
        self.coins = 0

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
        
    def handle_collision(self, obj):
        self.collision_handler.handle_collision(self, obj)