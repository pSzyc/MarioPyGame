from abc import ABC, abstractmethod
from events import EventManager
import sys
sys.path.append('..')
from utilities.initalize import Initalizer
import pygame

class AbstractGameManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def stop(self):
        pass

class GameManager(AbstractGameManager):
    def __init__(self, initalizer):
        super().__init__()
        self.event_manager = EventManager()
        self.initalizer = initalizer
        world = self.initalizer.initalize()
        self.world = world

    def step(self):
        self.world.gravity()
        self.world.move_actors()
        outcome = self.event_manager.handle_events(world)
        if outcome == 'Lose':
            print('You lose')
            pygame.quit()
            sys.exit()
        elif outcome == 'Win':
            print('You win')
            pygame.quit()
            sys.exit()
        else:
            self.world.draw()