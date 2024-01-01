import pygame
from abc import ABC, abstractmethod

GREEN = (34, 139, 34)

class GameObject(ABC):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._image = image

    @abstractmethod
    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        pass

    @property
    def image(self) -> pygame.Surface:
        return self._image
    
    @image.setter
    def image(self, value: pygame.Surface) -> None:
        self._image = value

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, value: int) -> None:
        self._y = value

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        self._width = value
    
    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def rectangle(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, value: int) -> None:
        self._x = value

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, value: int)  -> None:
        self._y = value

    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, value: int) -> None:
        self._width = value
    
    @property
    def height(self) -> int:
        return self._height
    
    @height.setter
    def height(self, value: int) -> None:
        self._height = value


class Coin(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Cherry(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Chest(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Door(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Ground(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def grass(self, x_offset, y_offset) -> pygame.Rect:
        return pygame.Rect(self.x - x_offset, self.y - y_offset, self._width, 10)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        for x in range(self.rectangle.x - x_offset, self.rectangle.x - x_offset + self.width, self.image.get_width()):
            for y in range(self.rectangle.y - y_offset, self.rectangle.y - y_offset + self.height, self.image.get_height()):
                screen.blit(self.image, (x, y))
                # Draw grass
        pygame.draw.rect(screen, GREEN, self.grass(x_offset, y_offset))

class Boundary(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface = None) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        pass

class Wine(GameObject):
    def __init__(self, x: int, y: int, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect: pygame.Rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)
