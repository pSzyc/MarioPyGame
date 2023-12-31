import pygame
from abc import ABC, abstractmethod

GREEN = (34, 139, 34)

class GameObject(ABC):
    def __init__(self, x, y, width, height, image):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._image = image

    @abstractmethod
    def draw(self, screen, x_offset, y_offset):
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

    def draw(self, screen, x_offset, y_offset):
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Cherry(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen, x_offset, y_offset):
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Chest(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen, x_offset, y_offset):
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Door(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen, x_offset, y_offset):
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Ground(GameObject):
    def __init__(self, x, y, width, height, texture_image):
        texture_width = texture_image.get_width()
        texture_height = texture_image.get_height()
        width = width - width % texture_width
        height = height - height % texture_height
        self.texture_width = texture_width
        self.texture_height = texture_height  
        super().__init__(x, y, width, height, texture_image)

    def grass(self, x_offset, y_offset):
        return pygame.Rect(self.x - x_offset, self.y - y_offset, self._width, 10)

    def draw(self, screen, x_offset, y_offset):
        for x in range(self.rectangle.x - x_offset, self.rectangle.x - x_offset + self.width, self.image.get_width()):
            for y in range(self.rectangle.y - y_offset, self.rectangle.y - y_offset + self.height, self.image.get_height()):
                screen.blit(self.image, (x, y))
                # Draw grass
        pygame.draw.rect(screen, GREEN, self.grass(x_offset, y_offset))

class Boundary(GameObject):
    def __init__(self, x, y, width, height, image = None):
        super().__init__(x, y, width, height, image)

    def draw(self, screen, x_offset, y_offset):
        if self.image:
            draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
            screen.blit(self.image, draw_rect)

class Wine(GameObject):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)

    def draw(self, screen, x_offset, y_offset):
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)