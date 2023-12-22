from abc import ABC, abstractmethod
from math import sqrt
from actors import Mario, Ghost
from objects import Coin, Cherry, Chest
from ground import ground

class Event(ABC):
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

    @abstractmethod
    def handle(self):
        pass

class EventDispatcher:
    def __init__(self):
        mario_event_dict = {
            ground.__name__: MarioHitsGroundEvent,
            Coin.__name__: MarioHitsCoinEvent,
            Cherry.__name__: MarioHitsCherryEvent,
            Chest.__name__: MarioHitsChestEvent,
            Ghost.__name__: MarioHitGhostEvent
        }
        ghost_event_dict = {
            ground.__name__: GhostHitsGroundEvent,
        }
        self.nested_event_dict = {
            Mario.__name__: mario_event_dict,
            Ghost.__name__: ghost_event_dict
        }

    def dispatch(self, actor, object):
        actor_event_dict = self.nested_event_dict[actor.__class__.__name__]
        event = actor_event_dict[object.__class__.__name__](actor, object)
        return event

    def register_event(self, event_name, actor_event_dict):
        self.event_dict[event_name] = actor_event_dict
    

class EventManager:
    def __init__(self, actors):
        self.events = []
        self.actors = actors

    def add_event(self, event):
        self.events.append(event)

    def handle_events(self):
        for event in self.events:
            actor = event.handle()
            if event.handle():
                self.actors.remove(actor)

class MarioHitsGroundEvent(Event):    
    def handle(self):
        self.obj1.handle_collision(self.obj2.rectangle)
        if self.obj1.speed_x > 0.1:
            self.obj1.speed_x -= 0.1
        elif self.obj1.speed_x < -0.1:
            self.obj1.speed_x += 0.1
        else:
            self.obj1.speed_x = 0

class GhostHitsGroundEvent(Event):
    def handle(self):
        self.obj1.handle_collision(self.obj2.rectangle)

class MarioHitsCoinEvent(Event):    
    def handle(self):
        self.obj1.coins += 1
        return self.obj2

class MarioHitsCherryEvent(Event):
    def handle(self):
        self.obj1.lifes += 1
        return self.obj2

class MarioHitsChestEvent(Event):
    def handle(self):
        self.obj1.coins += 10
        return self.obj2

class MarioHitGhostEvent(Event):
    def handle(self):
        self.obj1.handle_collision(self.obj2.rectangle)
        self.obj2.handle_collision(self.obj1.rectangle)
        if self.obj2 is not None:        
            self.push_mario()
            return 

    def push_mario(self):
        x_d = self.obj1.x - self.obj2.x
        y_d = self.obj1.y - self.obj2.y
        norm = sqrt((x_d) ** 2 + (y_d) ** 2)
        x_d = x_d / norm
        y_d = y_d / norm
        self.obj1.speed_x = 10 * x_d
        self.obj1.speed_y = 10 * y_d