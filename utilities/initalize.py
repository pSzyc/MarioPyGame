from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from game_components.game_object_factory import ObjectFactory
from game_components.actors import *
from game_components.game_objects import *
from game_components.world import World

class Initalizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initalize(self):
        pass
        

class RefrenceFromFileInitalizer(Initalizer):
    def __init__(self, filename : str) -> None:
        self.filename = filename
        self.x_ref = 0
        self.y_ref = 0

    def initalize(self) -> None:
        with open(self.filename, 'r') as f:
            content = f.read()
        factory = ObjectFactory()
        world = World()
        world.initalize()
        commands = content.split('\n')
        for command in commands:
            command = command.split(' ')
            if command[0] == '//': continue
            obj_class = command[0]
            obj_args = command[1:]
            
            if obj_class == 'Ground':
                # setting frame of refrence
                self.x_ref = int(obj_args[0])
                self.y_ref = int(obj_args[1])
            else:
                # new coordinates for non ground objects
                obj_args[0] = str(int(obj_args[0]) + self.x_ref)
                obj_args[1] = str(int(obj_args[1]) + self.y_ref)
            
            if 'chase' in obj_args:
                if world.mario:
                    obj_args.append(world.mario)
                else:
                    raise ValueError('Mario must be initalized before any actors that chase him')
            
            obj = factory.create(obj_class, obj_args)
            if obj_class == Mario.__name__:
                world.mario = obj
            
            world.add_new(obj)
        return world