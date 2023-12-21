from abc import ABC, abstractmethod
from math import sqrt
class Event(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle(self):
        pass


class EventManager:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def handle_events(self):
        for event in self.events:
            event.handle()
        self.events = []

class ObjectsCollisionEvent(Event):
    def __init__(self, obj1, obj2):
        super().__init__()
        self.obj1 = obj1
        self.obj2 = obj2

    def handle(self):
        self.obj1.handle_collision(self.obj2.rectangle)
        self.obj2.handle_collision(self.obj1.rectangle)

class MarioHitGhostEvent(Event):
    def __init__(self, mario, ghost):
        super().__init__()
        self.mario = mario
        self.ghost = ghost

    def handle(self):
        self.mario.handle_collision(self.ghost.rectangle)
        self.ghost.handle_collision(self.mario.rectangle)
        x_d = self.mario.x - self.ghost.x
        y_d = self.mario.y - self.ghost.y
        norm = sqrt((x_d) ** 2 + (y_d) ** 2)
        x_d = x_d / norm
        y_d = y_d / norm
        self.mario.speed_x = 10 * x_d
        self.mario.speed_y = 10 * y_d

class MarioHitsGroundEvent(Event):
    def __init__(self, mario, ground):
        super().__init__()
        self.mario = mario
        self.ground = ground

    def handle(self):
        self.mario.handle_collision(self.ground.rectangle)
        self.ground.handle_collision(self.mario.rectangle)
        self.mario.speed_y = 0
        self.mario.speed_x = 0


class CollisionHandler(ABC):
    def __init__(self, actor, obj):
        pass

    @abstractmethod
    def hit_from_bottom(self):
        pass

    @abstractmethod
    def hit_from_top(self):
        pass

    @abstractmethod
    def hit_from_left(self):
        pass

    @abstractmethod
    def hit_from_right(self):
        pass

    def handle_collision(self):
        if self.actor.y + self.actor.height / 2 > self.obj.top and self.actor.y_prev + self.actor.height / 2 <= self.obj.top:
            self.hit_from_bottom()

        elif self.actor.y - self.actor.height / 2 < self.obj.bottom and self.actor.y_prev - self.actor.height / 2 >= self.obj.bottom:
            self.hit_from_top()
        
        if self.actor.x + self.actor.width / 2 > self.obj.left and self.actor.x_prev + self.actor.width / 2 <= self.obj.left:
            self.hit_from_left()

        elif self.actor.x - self.actor.width / 2 < self.obj.right and self.actor.x_prev - self.actor.width / 2 >= self.obj.right:
            self.hit_from_right()