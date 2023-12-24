from abc import ABC, abstractmethod
from math import sqrt
from actors import Mario, Ghost, Actor
from objects import Coin, Cherry, Chest
from ground import Ground
from objects import GameObject

class Event(ABC):
    def __init__(self, obj1, obj2):
        self.obj1 = obj1
        self.obj2 = obj2

    @abstractmethod
    def handle(self):
        pass

class CollisionEvent(Event):
    @property
    def actor(self):
        return self.obj1
    
    @property
    def object(self):
        return self.obj2.rectangle

    def hit_from_bottom(self):
        self.actor.y = self.object.top - self.actor.height / 2
        self.actor.speed_y = 0

    def hit_from_top(self):
        self.actor.y = self.object.bottom + self.actor.height / 2
        self.actor.speed_y = 0

    def hit_from_left(self):
        self.actor.x = self.object.left - self.actor.width / 2
        self.actor.speed_x = 0

    def hit_from_right(self):
        self.actor.x = self.object.right + self.actor.width / 2
        self.actor.speed_x = 0

    def handle(self):
        self.bottom = (self.actor.rectangle.bottom > self.object.top) and (self.actor.prev_rectangle.bottom <= self.object.top)
        self.top = (self.actor.rectangle.top < self.object.bottom) and (self.actor.prev_rectangle.top >= self.object.bottom)
        self.left = (self.actor.rectangle.right > self.object.left) and (self.actor.prev_rectangle.right <= self.object.left)
        self.right = (self.actor.rectangle.left < self.object.right) and (self.actor.prev_rectangle.left >= self.object.right)
        if self.top: self.hit_from_top()
        if self.bottom: self.hit_from_bottom()
        if self.left: self.hit_from_left()
        if self.right: self.hit_from_right()

class EventDispatcher:
    def __init__(self):
        mario_event_dict = {
            Ground.__name__: MarioHitsGroundEvent,
            Coin.__name__: MarioHitsCoinEvent,
            Cherry.__name__: MarioHitsCherryEvent,
            Chest.__name__: MarioHitsChestEvent,
            Ghost.__name__: MarioHitsGhostEvent
        }
        ghost_event_dict = {
            Ground.__name__: CollisionEvent,
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
    def __init__(self, objects, actors):
        self.events = []
        self.actors = actors
        self.objects = objects

    def add_event(self, event):
        self.events.append(event)

    def handle_events(self):
        for event in self.events:
            obj = event.handle()
            if isinstance(obj, Actor):
                self.actors.remove(obj)
            elif isinstance(obj, GameObject):
                self.objects.remove(obj)


class MarioHitsGroundEvent(CollisionEvent):    
    def hit_from_bottom(self):
        super().hit_from_bottom()
        self.actor.jump_energy = 27.5
        if self.actor.speed_x > 0.5:
            self.actor.speed_x -= 0.5
        elif self.actor.speed_x < -0.5:
            self.actor.speed_x += 0.5
        else:
            self.actor.speed_x = 0

class MarioHitsGhostEvent(CollisionEvent):
    def handle(self):
        super().handle()
        if self.bottom:
            return self.obj2
        else:
            self.actor.lifes -= 1
            self.push_mario()
            if self.actor.lifes == 0:
                return self.actor
    
    def push_mario(self):
        dx = self.actor.x - self.obj2.x
        dy = self.actor.y - self.obj2.y
        d = sqrt(dx**2 + dy**2)
        self.actor.speed_x = dx / d * 10
        self.actor.speed_y = dy / d * 10
        self.actor.stunned_time = 10
        

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