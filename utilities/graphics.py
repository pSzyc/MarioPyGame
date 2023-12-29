import pygame
from abc import ABC, abstractmethod

class ImageLoader(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def load_image(self):
        pass

class FromFileLoader(ImageLoader):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def load_image(self, width, height):
        image = pygame.image.load(self.filename)
        image = pygame.transform.scale(image, (width, height))
        image.convert()
        return image