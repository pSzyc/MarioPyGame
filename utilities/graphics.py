import pygame
from abc import ABC, abstractmethod

class ImageLoader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_image(self) -> pygame.Surface:
        pass

class FromFileLoader(ImageLoader):
    __slots__ = ['_filename']
    def __init__(self, filename: str) -> None:
        super().__init__()
        self._filename = filename

    def load_image(self, width: int, height: int) -> pygame.Surface:
        image = pygame.image.load(self._filename)
        image = pygame.transform.scale(image, (width, height))
        image.convert()
        return image