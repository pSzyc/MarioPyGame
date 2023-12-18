import numpy as np
from abc import ABC, abstractmethod
import pygame
import random
from move import BackAndForthMoveStrategy, ChaseMoveStrategy, ControlMoveStrategy
class Actor(ABC):
    def __init__(self, x, y, width, height, filename):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._filename = filename
        self._image = None

    @property
    def filename(self):
        return self._filename
    
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, value):
        self._image = value

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
    def on_turn(self, isRight):
        pass

    @abstractmethod
    def init_image(self):
        pass

    @abstractmethod
    def init_image(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def handle_collision(self, ground):
        pass

class Ghost(Actor):
    def __init__(self, x, y, width=40, height=40, filename = "mario_ghost.png"):
        super().__init__(x, y, width=width, height=height, filename=filename)
        self.image = self.init_image()
        self.speed_y = 0
        self.speed_x = 2.5
        self.move_strategy = BackAndForthMoveStrategy(self)
        self.right = True

    def init_image(self):
        image = pygame.image.load(self.filename)
        image = pygame.transform.scale(image, (self.width, self.height))
        image.convert()
        return image
    
    def on_turn(self, isRight):
        self.right = isRight
        self.image = pygame.transform.flip(self.image, True, False)

    def handle_collision(self, ground):
        # handle y collision       
        if self.y + self.height / 2 > ground.top and self.y_prev + self.height / 2 <= ground.top:
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
        self.move_strategy.make_move()

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class Mario(Actor):
    def __init__(self, x, y, width=40, height=60, filename = "mario.webp"):
        super().__init__(x, y, width=width, height=height, filename=filename)
        self.speed_y = 0
        self.speed_x = 5
        self.image = self.init_image()
        self.right = True
        self.move_strategy = ControlMoveStrategy(self)
        self.jump_energy = 0

    def init_image(self):
        image = pygame.image.load(self.filename)
        image = pygame.transform.scale(image, (self.width, self.height))
        image.convert()
        return image
    
    def on_turn(self, isRight):
        if self.right != isRight:
            self.right = not self.right
            self.image = pygame.transform.flip(self.image, True, False)
    
    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def move(self):
        self.move_strategy.make_move()

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