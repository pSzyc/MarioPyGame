import pygame
from move import *
from itertools import combinations
from actors_factory import *
from events import EventDispatcher, EventManager
from time import sleep
from initalize import RefrenceFromStringInitalizer

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

    def initalize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        with open('resources/board.txt', 'r') as f:
            board = f.read()
        initalizer = RefrenceFromStringInitalizer(board)
        initalizer.initalize(world=self)

    def add_ground(self, ground):
        self.ground_objects.append(ground)
    
    def add_actor(self, actor):
        self.actors.append(actor)

    def add_object(self, obj):
        self.objects.append(obj)

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
        x_offset = self.mario.x - self.mario.x_prev
        y_offset = self.mario.y - self.mario.y_prev
        if self.mario.x < self._camera_left_barier or self.mario.x > self._camera_right_barier:
            x_offset = 0

        for actor in self.actors:
            actor.x -= x_offset
            actor.y -= y_offset
        for obj in self.objects:
            obj.x -= x_offset
            obj.y -= y_offset
        for ground in self.ground_objects:
            ground.x -= x_offset
            ground.y -= y_offset
        self._camera_left_barier -= x_offset
        self._camera_right_barier -= x_offset


    def camera_adjust_mario(self):
        x_offset = int(self.mario.x - self.screen.get_width() / 2)
        y_offset = int(self.mario.y - self.screen.get_height() / 2)
        return x_offset, y_offset

    def draw(self):
        self.screen.fill((150, 150, 200))  # Light blue background color
        x_offset, y_offset = self.camera_adjust_mario()
        self.draw_scene(x_offset, y_offset)
        pygame.display.update()