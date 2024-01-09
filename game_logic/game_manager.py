from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from game_logic.events import EventDispatcher, MarioHitsDoorEvent
from game_components.actors import Mario, GameObject, Actor
from game_components.world import World

class AbstractGameManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def step(self) -> str:
        pass

class GameManager(AbstractGameManager):

    __slots__ = ['_world', '_event_dispatcher', '_events']
    def __init__(self, world: World):
        super().__init__()
        self._world = world
        self._event_dispatcher = EventDispatcher()
        self._events = []
    
    @property
    def world(self) -> World:
        return self._world

    def register_events(self):
        self.events = []
        # mario interacting with other actors
        for actor in self.world.actors:
            if actor == self.world.mario:
                continue
            if self.world.mario.rectangle.colliderect(actor.rectangle):
                self.events.append(self._event_dispatcher.dispatch(self.world.mario, actor))

        # mario interacting with objects
        for obj in self.world.objects:
            if self.world.mario.rectangle.colliderect(obj.rectangle):
                self.events.append(self._event_dispatcher.dispatch(self.world.mario, obj))

        # actors interacting with objects
        for actor in self.world.actors:
            for ground in self.world.ground_objects:
                if actor.rectangle.colliderect(ground.rectangle):
                    self.events.append(self._event_dispatcher.dispatch(actor, ground))
    
    def remove_from_world(self, obj: GameObject) -> None:
        if isinstance(obj, Actor):
            self.world.actors.remove(obj)
        elif isinstance(obj, GameObject):
            self.world.objects.remove(obj)
        else:
            raise ValueError('Event returned invalid object')
    
    def handle_events(self) -> str:
        for event in self.events:
            obj = event.handle()
            if isinstance(event, MarioHitsDoorEvent):
                return 'Win'
            elif obj:
                self.remove_from_world(obj)
                if isinstance(obj, Mario):
                    return 'Lose'
        self.events = []
        return 'Continue'

    def step(self):
        self.world.gravity()
        self.world.move_actors()
        self.world.draw()
        self.register_events()
        outcome = self.handle_events()
        return outcome