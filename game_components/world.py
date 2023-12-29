import pygame
import sys
sys.path.append('..')
from game_logic.move import *
from game_components.game_object_factory import *
from game_logic.events import EventDispatcher, EventManager
from utilities.initalize import RefrenceFromStringInitalizer

class World:
    def __init__(self):
        self.mario = None
        self.screen = None
        self.ground_objects = []
        self.objects = []
        self.actors = []
        self._gravity = 1.5
        self.event_dispatcher = EventDispatcher()
        self._camera_left_barier = 400
        self._camera_right_barier = 4240

    def initalize(self, screen_width = 800, screen_height = 600, filename = 'resources/board.txt'):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        with open(filename, 'r') as f:
            board = f.read()
        initalizer = RefrenceFromStringInitalizer(board)
        initalizer.initalize(world=self)

    def add_ground(self, ground):
        self.ground_objects.append(ground)
    
    def add_actor(self, actor):
        self.actors.append(actor)

    def add_object(self, obj):
        self.objects.append(obj)

    def add_new(self, obj):
        if isinstance(obj, Actor):
            self.add_actor(obj)
        elif isinstance(obj, Ground):
            self.add_ground(obj)
        elif isinstance(obj, GameObject):
            self.add_object(obj)
        else:
            raise TypeError('Object is not a valid type')

    def move_actors(self):
        for actor in self.actors:
            actor.move()
    
    def draw_scene(self, x_offset, y_offset):
        for actor in self.actors:
            actor.draw(self.screen, x_offset, y_offset)
        for obj in self.objects:
            obj.draw(self.screen, x_offset, y_offset)
        for ground in self.ground_objects:
            ground.draw(self.screen, x_offset, y_offset)

    def handle_collision(self):
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
        

    def gravity(self):
        for actor in self.actors:
            actor.gravity(self._gravity)

    def camera_adjust(self):
        x_offset = int(self.mario.x - self.screen.get_width() / 2)
        y_offset = int(self.mario.y - self.screen.get_height() / 2)
        return x_offset, y_offset

    def draw(self):
        self.screen.fill((150, 150, 200))  # Light blue background color
        x_offset, y_offset = self.camera_adjust()
        self.draw_scene(x_offset, y_offset)
        pygame.display.update()