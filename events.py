from abc import ABC, abstractmethod
from math import sqrt
from actors import Mario, Ghost
from objects import Coin, Cherry, Chest
from world import ground

class Event(ABC):
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

    @abstractmethod
    def handle(self):
        pass

class EventDispatcher:
    def __init__(self):
        self.event_dict = {
            ground.__class__.__name__: MarioHitsGroundEvent,
            Coin.__class__.__name__: MarioHitsCoinEvent,
            Cherry.__class__.__name__: MarioHitsCherryEvent,
            Chest.__class__.__name__: MarioHitsChestEvent,
            Ghost.__class__.__name__: MarioHitGhostEvent
        }

    def dispatch(self, mario, object):
        event_class = self.event_dict[object.__class__.__name__]
        event = event_class(mario, object)
        return event

    def register_event(self, event_name, event_class):
        self.event_dict[event_name] = event_class
    

class EventManager:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def handle_events(self):
        for event in self.events:
            event.handle()
        self.events = []

class MarioHitsGroundEvent(Event):    
    def handle(self):
        self.mario.jump_energy = 20
        self.mario.speed_x -= (2 * self.mario.speed_x > 0 - 1) * self.ground.friction
        self.mario.handle_collision(self.ground.rectangle)

class MarioHitsCoinEvent(Event):    
    def handle(self):
        self.mario.coins += 1
        del self.coin

class MarioHitsCherryEvent(Event):
    def handle(self):
        self.mario.lives += 1
        del self.cherry

class MarioHitsChestEvent(Event):
    def handle(self):
        self.mario.coins += 10
        del self.chest

class MarioHitGhostEvent(Event):
    def __init__(self, mario, ghost):
        super().__init__()
        self.mario = mario
        self.ghost = ghost

    def handle(self):
        self.mario.handle_collision(self.ghost.rectangle)
        self.ghost.handle_collision(self.mario.rectangle)
        if self.ghost is not None:        
            self.push_mario()

    def push_mario(self):
        x_d = self.mario.x - self.ghost.x
        y_d = self.mario.y - self.ghost.y
        norm = sqrt((x_d) ** 2 + (y_d) ** 2)
        x_d = x_d / norm
        y_d = y_d / norm
        self.mario.speed_x = 10 * x_d
        self.mario.speed_y = 10 * y_d