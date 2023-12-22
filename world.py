import pygame
from move import *
from itertools import combinations
from actors_factory import *
from events import EventDispatcher, EventManager
from ground import ground
from time import sleep

class World:
    def __init__(self):
        self.mario = None
        self.screen = None
        self.ground_objects = []
        self.objects = []
        self.actors = []
        self._gravity = 1
        self.event_dispatcher = EventDispatcher()

    def initalize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.init_actors()
        self.init_ground()

    def init_ground(self):
        self.add_ground(ground(0, 500, 400, 100))
        self.add_ground(ground(400, 300, 400, 300))

    def init_actors(self):
        mario_maker = MarioMaker()
        coin_maker = CoinMaker()
        cherry_maker = CherryMaker()
        chest_maker = ChestMaker()
        ghost_maker = GhostMaker()
        self.mario = mario_maker.create_actor(100, 100, 5, 0, 40, 60)
        ghost = ghost_maker.create_actor(500, 100, 5, 0, 'chase', 40, 40, mario=self.mario)
        coin = coin_maker.create_actor(400, 250, 40, 40)
        cherry = cherry_maker.create_actor(500, 250, 40, 40)
        chest = chest_maker.create_actor(600, 250, 40, 40)
        self.add_actor(self.mario)
        #self.add_actor(ghost)
        #self.add_object(ghost)
        self.add_object(coin)
        self.add_object(cherry)
        self.add_object(chest)

    def add_ground(self, ground):
        self.ground_objects.append(ground)
    
    def add_actor(self, actor):
        self.actors.append(actor)

    def add_object(self, obj):
        self.objects.append(obj)

    def move_actors(self):
        for actor in self.actors:
            actor.move()
    
    def draw_actors(self):
        for actor in self.actors:
            actor.draw(self.screen)
        for obj in self.objects:
            obj.draw(self.screen)

    def handle_collision(self):
        event_manager = EventManager(self.objects)
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
        
        event_manager.handle_events()


    def gravity(self):
        for actor in self.actors:
            actor.gravity(self._gravity)

    def draw_gorund(self):
        for ground in self.ground_objects:
            ground.draw(self.screen)

    def draw(self):
        self.screen.fill((100, 100, 255))
        self.draw_actors()
        self.draw_gorund()
        pygame.display.update()