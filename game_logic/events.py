from abc import ABC, abstractmethod
from math import sqrt
import sys
sys.path.append('..')
from game_components.actors import *
from game_components.game_objects import *
from typing import List

class Event(ABC):
    __slots__ = ['_obj1', '_obj2']
    def __init__(self, obj1: GameObject, obj2: GameObject):
        self._obj1 = obj1
        self._obj2 = obj2
    
    @property
    def obj1(self) -> GameObject:
        return self._obj1
    
    @property
    def obj2(self) -> GameObject:
        return self._obj2

    @abstractmethod
    def handle(self) -> None:
        pass

class CollisionEvent(Event):
    @property
    def actor(self) -> Actor:
        return self.obj1
    
    @property
    def object(self) -> pygame.Rect:
        return self.obj2.rectangle

    def hit_from_bottom(self) -> None:
        self.actor.y = self.object.top - self.actor.height
        self.actor.speed_y = 0

    def hit_from_top(self) -> None:
        self.actor.y = self.object.bottom
        self.actor.speed_y = 0

    def hit_from_left(self) -> None:
        self.actor.x = self.object.right
        self.actor.speed_x = 0

    def hit_from_right(self) -> None:
        self.actor.x = self.object.left - self.actor.width
        self.actor.speed_x = 0

    def handle(self) -> None:
        self.bottom = (self.actor.rectangle.bottom > self.object.top) and (self.actor.prev_rectangle.bottom <= self.object.top)
        self.top = (self.actor.rectangle.top < self.object.bottom) and (self.actor.prev_rectangle.top >= self.object.bottom)
        self.right = (self.actor.rectangle.right > self.object.left) and (self.actor.prev_rectangle.right <= self.object.left)
        self.left = (self.actor.rectangle.left < self.object.right) and (self.actor.prev_rectangle.left >= self.object.right)
        if self.top: self.hit_from_top()
        if self.bottom: self.hit_from_bottom()
        if self.left: self.hit_from_left()
        if self.right: self.hit_from_right()

class EventDispatcher:
    __slots__ = ['_nested_event_dict']    
    def __init__(self) -> None:
        mario_event_dict = {
            Ground.__name__: MarioHitsGroundEvent,
            Coin.__name__: MarioHitsCoinEvent,
            Cherry.__name__: MarioHitsCherryEvent,
            Chest.__name__: MarioHitsChestEvent,
            Ghost.__name__: MarioHitsGhostEvent,
            Boundary.__name__: ActorHitsBoundary,
            Door.__name__: MarioHitsDoorEvent,
            Wine.__name__: MarioHitsWineEvent,
            Bomb.__name__: MarioHitsBombEvent
        }
        ghost_event_dict = {
            Ground.__name__: CollisionEvent,
            Boundary.__name__: ActorHitsBoundary,
        }
        bomb_event_dict = {
            Ground.__name__: CollisionEvent,
            Boundary.__name__: ActorHitsBoundary,
        }
        self._nested_event_dict = {
            Mario.__name__: mario_event_dict,
            Ghost.__name__: ghost_event_dict,
            Bomb.__name__: bomb_event_dict
        }

    def dispatch(self, actor: Actor, object: GameObject) -> Event:
        actor_event_dict = self._nested_event_dict[actor.__class__.__name__]
        event = actor_event_dict[object.__class__.__name__](actor, object)
        return event

    def register_actor(self, actor_class: type, actor_event_dict: dict) -> None:
        self._nested_event_dict[actor_class] = actor_event_dict

    def register_event(self, actor_class: type, object_class: type, event_class: type) -> None:
        self._nested_event_dict[actor_class][object_class] = event_class

class MarioHitsGroundEvent(CollisionEvent):    
    def hit_from_bottom(self) -> None:
        super().hit_from_bottom()
        self.actor.jump_energy = 27.5

        if self.actor.speed_x > 0.5:
            self.actor.speed_x -= 0.5
        elif self.actor.speed_x < -0.5:
            self.actor.speed_x += 0.5
        else:
            self.actor.speed_x = 0

class ActorHitsBoundary(Event):
    def handle(self) -> GameObject:
        return self.obj1

class MarioHitsGhostEvent(CollisionEvent):
    def handle(self) -> GameObject:
        super().handle()
        if self.bottom:
            return self.obj2
        else:
            self.actor.lifes -= 1
            self.push_mario()
            if self.actor.lifes == 0:
                return self.actor
    
    def push_mario(self) -> None:
        dx = self.actor.x - self.obj2.x
        dy = self.actor.y - self.obj2.y
        d = sqrt(dx**2 + dy**2)
        self.actor.speed_x = dx / d * 10
        self.actor.speed_y = dy / d * 10
        self.actor.stunned_time = 10
        

class MarioHitsCoinEvent(Event):    
    def handle(self) -> GameObject:
        self.obj1.coins += 1
        return self.obj2

class MarioHitsCherryEvent(Event):
    def handle(self) -> GameObject:
        self.obj1.lifes += 1
        return self.obj2

class MarioHitsChestEvent(Event):
    def handle(self) -> GameObject:
        self.obj1.coins += 10
        return self.obj2
    
class MarioHitsDoorEvent(Event):
    def handle(self) -> None:
        return 
    
class MarioHitsWineEvent(Event):
    def handle(self) -> GameObject:
        self.obj1.lifes += 1
        self.obj1.stunned_time += 100
        self.obj1.fall_asleep()
        return self.obj2
    
class MarioHitsBombEvent(Event):
    def handle(self)-> GameObject:
        self.obj1.lifes -= 1
        self.obj1.stunned_time += 100
        self.obj1.fall_asleep()
        self.push_mario()
        return self.obj2
    
    def push_mario(self) -> None:        
        dx = self.obj1.x - self.obj2.x
        dy = self.obj1.y - self.obj2.y
        d = sqrt(dx**2 + dy**2)
        self.obj1.speed_x = dx / d * 40
        self.obj1.speed_y = dy / d * 40