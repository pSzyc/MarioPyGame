import pygame
import sys
sys.path.append('..')
from game_logic.move import *
from game_components.game_object_factory import *
from game_logic.events import EventDispatcher, EventManager
from utilities.initalize import RefrenceFromStringInitalizer
from typing import List, Optional, Tuple
import pygame
import sys
from game_logic.move import *
from game_components.game_object_factory import *
from game_logic.events import EventDispatcher, EventManager
from utilities.initalize import RefrenceFromStringInitalizer

class World:
    def __init__(self):
        self.mario: Optional[Actor] = None
        self.screen: Optional[pygame.Surface] = None
        self.ground_objects: List[Ground] = []
        self.objects: List[GameObject] = []
        self.actors: List[Actor] = []
        self._gravity: float = 1.5
        self.event_dispatcher: EventDispatcher = EventDispatcher()
        self._camera_left_barier: int = 400
        self._camera_right_barier: int = 4240

    def initalize(self, screen_width: int = 800, screen_height: int = 600, filename: str = 'resources/board.txt') -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        with open(filename, 'r') as f:
            board = f.read()
        initalizer = RefrenceFromStringInitalizer(board)
        initalizer.initalize(world=self)

    def add_ground(self, ground: Ground) -> None:
        self.ground_objects.append(ground)

    def add_actor(self, actor: Actor) -> None:
        self.actors.append(actor)

    def add_object(self, obj: GameObject) -> None:
        self.objects.append(obj)

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
        for actor in self.actors:
            actor.move()

    def draw_scene(self, x_offset: int, y_offset: int) -> None:
        for actor in self.actors:
            actor.draw(self.screen, x_offset, y_offset)
        for obj in self.objects:
            obj.draw(self.screen, x_offset, y_offset)
        for ground in self.ground_objects:
            ground.draw(self.screen, x_offset, y_offset)

    def handle_collision(self) -> str:
        event_manager = EventManager(self.objects, self.actors)
        for actor in self.actors:
            if actor == self.mario:
                continue
            if self.mario.rectangle.colliderect(actor.rectangle):
                event_manager.add_event(self.event_dispatcher.dispatch(self.mario, actor))
                
        for obj in self.objects:
            if self.mario.rectangle.colliderect(obj.rectangle):
                event_manager.add_event(self.event_dispatcher.dispatch(self.mario, obj))

        for actor in self.actors:
            for ground in self.ground_objects:
                if actor.rectangle.colliderect(ground.rectangle):
                    event_manager.add_event(self.event_dispatcher.dispatch(actor, ground))
        
        outcome = event_manager.handle_events()
        return outcome
        

    def gravity(self) -> None:
        for actor in self.actors:
            actor.gravity(self._gravity)

    def camera_adjust(self) -> Tuple[int, int]:
        x_offset = int(self.mario.x - self.screen.get_width() / 2)
        y_offset = int(self.mario.y - self.screen.get_height() / 2)
        return x_offset, y_offset

    def draw(self) -> None:
        self.screen.fill((150, 150, 200))  # Light blue background color
        x_offset, y_offset = self.camera_adjust()
        self.draw_scene(x_offset, y_offset)
        pygame.display.update()