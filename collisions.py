from abc import ABC, abstractmethod
from ground import ground

class AbstractCollisionHandler(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def handle_collision(self, actor, obj):
        pass

class ActorCollisionHandler(AbstractCollisionHandler):
    def hit_from_bottom(self, actor, obj):
        actor.y = obj.top - actor.height / 2
        actor.speed_y = 0

    def hit_from_top(self, actor, obj):
        actor.y = obj.bottom + actor.height / 2
        actor.speed_y = 0

    def hit_from_left(self, actor, obj):
        actor.x = obj.left - actor.width / 2
        actor.speed_x = 0

    def hit_from_right(self, actor, obj):
        actor.x = obj.right + actor.width / 2
        actor.speed_x = 0

    def handle_collision(self, actor, obj):
        if actor.y + actor.height / 2 > obj.top and actor.y_prev + actor.height / 2 <= obj.top:
            self.hit_from_bottom(actor, obj)

        elif actor.y - actor.height / 2 < obj.bottom and actor.y_prev - actor.height / 2 >= obj.bottom:
            self.hit_from_top(actor, obj)
        
        if actor.x + actor.width / 2 > obj.left and actor.x_prev + actor.width / 2 <= obj.left:
            self.hit_from_left(actor, obj)

        elif actor.x - actor.width / 2 < obj.right and actor.x_prev - actor.width / 2 >= obj.right:
            self.hit_from_right(actor, obj)

class GhostCollisionHandler(ActorCollisionHandler):
    def hit_from_top(self, actor, obj):
        del actor

class MarioCollisionHandler(ActorCollisionHandler):
    def hit_from_bottom(self, actor, obj):
        super().hit_from_bottom(actor, obj)
        actor.jump_energy = 20

class FragileCollisionHandler(AbstractCollisionHandler):
    def handle_collision(self, actor, obj):
        del actor
