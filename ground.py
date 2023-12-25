import pygame
from math import ceil

GREEN = (34, 139, 34)

class Ground:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        width = width - width % 40
        height = height - height % 40
        self._width = width
        self._height = height
        self.texture_width = 40
        self.texture_height = 40  
        self.texture = pygame.image.load("resources/ground.png")
        self.texture = pygame.transform.scale(self.texture, (self.texture_width, self.texture_height))
    

    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, x):
        self._x = x

    @y.setter
    def y(self, y):
        self._y = y

    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def grass(self):
        return pygame.Rect(self.x, self.y, self._width, 10)

    def draw(self, screen):
        # Draw the ground
        for x in range(self.rectangle.x, self.rectangle.x+ self.width, self.texture.get_width()):
            for y in range(self.rectangle.y, self.rectangle.y + self.height, self.texture.get_height()):
                screen.blit(self.texture, (x, y))
                # Draw grass
        pygame.draw.rect(screen, GREEN, self.grass())
