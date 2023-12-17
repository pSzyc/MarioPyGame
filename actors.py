import numpy as np
from abc import ABC, abstractmethod
import pygame

class Actor(ABC):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height

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

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height
    
    @property
    def rectangle(self):
        return pygame.Rect(self.x - self.width / 2, self.y - self.height / 2, self.width, self.height)
    
    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass
    10
    @abstractmethod
    def handle_collision(self, ground):
        pass

class Ghost(Actor):
    def __init__(self, x, y):
        super().__init__(x, y)

    def move(self):
        pass
    
    def draw(self, screen):
        pass

class Mario(Actor):
    def __init__(self, x, y, width=20, height=40):
        super().__init__(x, y, width=width, height=height)
        self.speed_y = 0
        self.shift_value = 5
        self.jump_energy = 0
        self.gravity = 1
        image = pygame.image.load("mario.webp")
        self.image = pygame.transform.scale(image, (self.width, self.height))
        self.image.convert()
        self.right = True

    def move(self):
        if self.jump_energy < 10:
            self.jump_energy += 0.5
        self.x_prev = self.x
        self.y_prev = self.y

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.shift_value
            if self.right:
                self.right = False
                self.image = pygame.transform.flip(self.image, True, False)
        if keys[pygame.K_RIGHT]:
            if not self.right:
                self.right = True
                self.image = pygame.transform.flip(self.image, True, False)
            self.x += self.shift_value
        if keys[pygame.K_UP]:
            if self.jump_energy >= 10:
                self.speed_y -= 10
                self.jump_energy -= 10
        
        self.y += self.speed_y
        self.speed_y += self.gravity


    def handle_collision(self, ground):
        # handle y collision       
        if self.y + self.height / 2 > ground.top and self.y_prev + self.height / 2 <= ground.top:
            self.y = ground.top - self.height / 2
            self.speed_y = 0
            self.jump_energy = 20
        elif self.y - self.height / 2 < ground.bottom and self.y_prev - self.height / 2 >= ground.bottom:
            self.speed_y = 0
            self.y = ground.bottom + self.height / 2
        # handle x collision
        if self.x + self.width / 2 > ground.left and self.x_prev + self.width / 2 <= ground.left:
            self.x = ground.left - self.width / 2
        elif self.x - self.width / 2 < ground.right and self.x_prev - self.width / 2 >= ground.right:
            self.x  = ground.right + self.width / 2
    def draw(self, screen):
        screen.blit(self.image, self.rectangle)