import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image

    @abstractmethod
    def draw(self, win):
        pass

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
    
    @width.setter
    def width(self, value):
        self._width = value
    
    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    @property
    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Coin(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class Cherry(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

class Chest(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)