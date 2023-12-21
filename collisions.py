from abc import ABC, abstractmethod
from world import ground

class AbstractCollisionHandler(ABC):
    def __init__(self, actor):
        self.actor = actor

    @abstractmethod
    def handle_collision(self, obj):
        pass

class ActorCollisionHandler(AbstractCollisionHandler):
    def hit_from_bottom(self, obj):
        self.actor.y = obj.top - self.actor.height / 2
        self.actor.speed_y = 0

    def hit_from_top(self, obj):
        self.actor.y = obj.bottom + self.actor.height / 2
        self.actor.speed_y = 0

    def hit_from_left(self, obj):
        self.actor.x = self.ground.left - self.actor.width / 2
        self.actor.speed_x = 0

    def hit_from_right(self, obj):
        self.actor.x = self.ground.right + self.actor.width / 2
        self.actor.speed_x = 0

    def handle_collision(self, obj):
        if self.actor.y + self.actor.height / 2 > obj.top and self.actor.y_prev + self.actor.height / 2 <= obj.top:
            self.hit_from_bottom()

        elif self.actor.y - self.actor.height / 2 < obj.bottom and self.actor.y_prev - self.actor.height / 2 >= obj.bottom:
            self.hit_from_top()
        
        if self.actor.x + self.actor.width / 2 > obj.left and self.actor.x_prev + self.actor.width / 2 <= obj.left:
            self.hit_from_left()

        elif self.actor.x - self.actor.width / 2 < obj.right and self.actor.x_prev - self.actor.width / 2 >= obj.right:
            self.hit_from_right()

class GhostCollisionHandler(ActorCollisionHandler):
    def hit_from_top(self):
        del self.actor

class FragileCollisionHandler(AbstractCollisionHandler):
    def handle_collision(self):
        del self.actor
