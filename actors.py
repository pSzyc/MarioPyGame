import numpy as np
from abc import ABC, abstractmethod
import pygame

class Actor(ABC):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

class Ghost(Actor):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self):
        pass
    
    def draw(self, screen):
        pass

class Mario(Actor):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 5
        self.rect = pygame.Rect(self.x - 5, self.y - 5, 10, 10)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def handle_collision(self, ground):
        if self.y + 5 < ground.top:
            self.y = ground.top - 5
        if self.y - 5 > ground.bottom:
            self.y = ground.bottom + 5
        if self.x + 5 < ground.left:
            self.x = ground.left - 5
        if self.x - 5 > ground.right:
            self.x = ground.right + 5
        
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), 5)