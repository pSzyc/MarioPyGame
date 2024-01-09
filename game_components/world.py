import pygame
import sys
sys.path.append('..')
from game_logic.move import *
from game_components.game_object_factory import *
from typing import List, Optional, Tuple
import pygame
import sys
from game_logic.move import *
from game_components.game_object_factory import *

class World:
    __slots__ = ['_mario', '_screen', '_ground_objects', '_objects', '_actors', '_gravity', '_camera_left_barier', '_camera_right_barier']
    def __init__(self):
        self._mario: Optional[Actor] = None
        self._screen: Optional[pygame.Surface] = None
        self._ground_objects: List[Ground] = []
        self._objects: List[GameObject] = []
        self._actors: List[Actor] = []
        self._gravity: float = 1.5
        self._camera_left_barier: int = 400
        self._camera_right_barier: int = 4240
    
    @property
    def mario(self) -> Actor:
        return self._mario
    
    @mario.setter
    def mario(self, mario: Actor) -> None:
        self._mario = mario
    
    @property
    def screen(self) -> pygame.Surface:
        return self._screen
    
    @property
    def ground_objects(self) -> List[Ground]:
        return self._ground_objects
    
    @property
    def objects(self) -> List[GameObject]:
        return self._objects
    
    @property
    def actors(self) -> List[Actor]:
        return self._actors

    def initalize(self, screen_width: int = 800, screen_height: int = 600) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((screen_width, screen_height))

    def add_ground(self, ground: Ground) -> None:
        self._ground_objects.append(ground)

    def add_actor(self, actor: Actor) -> None:
        self._actors.append(actor)

    def add_object(self, obj: GameObject) -> None:
        self._objects.append(obj)

    def add_new(self, obj: GameObject) -> None:
        if isinstance(obj, Actor):
            self.add_actor(obj)
        elif isinstance(obj, Ground):
            self.add_ground(obj)
        elif isinstance(obj, GameObject):
            self.add_object(obj)
        else:
            raise TypeError('Object is not a valid type')

    def move_actors(self) -> None:
        for actor in self._actors:
            actor.move()

    def draw_scene(self, x_offset: int, y_offset: int) -> None:
        for actor in self._actors:
            actor.draw(self.screen, x_offset, y_offset)
        for obj in self._objects:
            obj.draw(self.screen, x_offset, y_offset)
        for ground in self._ground_objects:
            ground.draw(self.screen, x_offset, y_offset)

    def gravity(self) -> None:
        for actor in self._actors:
            actor.gravity(self._gravity)

    def camera_adjust(self) -> Tuple[int, int]:
        x_offset = round(self.mario.x - self.screen.get_width() / 2)
        y_offset = round(self.mario.y - self.screen.get_height() / 2)
        return x_offset, y_offset

    def draw(self) -> None:
        self.screen.fill((150, 150, 200))  # Light blue background color
        x_offset, y_offset = self.camera_adjust()
        self.draw_scene(x_offset, y_offset)
        pygame.display.update()