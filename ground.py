import pygame
from objects import GameObject
GREEN = (34, 139, 34)

class Ground(GameObject):
    def __init__(self, x, y, width, height, texture_width = 40, texture_height = 40, texture = 'resources/ground.png'):
        width = width - width % texture_width
        height = height - height % texture_height
        self.texture_width = texture_width
        self.texture_height = texture_height  
        texture_image = pygame.image.load(texture)
        texture_image = pygame.transform.scale(texture_image, (self.texture_width, self.texture_height))
        super().__init__(x, y, width, height, texture_image)

    def grass(self):
        return pygame.Rect(self.x, self.y, self._width, 10)

    def draw(self, screen):
        for x in range(self.rectangle.x, self.rectangle.x+ self.width, self.image.get_width()):
            for y in range(self.rectangle.y, self.rectangle.y + self.height, self.image.get_height()):
                screen.blit(self.image, (x, y))
                # Draw grass
        pygame.draw.rect(screen, GREEN, self.grass())

class Boundary(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, None)

    def draw(self, screen):
        pass