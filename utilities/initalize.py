from abc import ABC, abstractmethod
import sys
sys.path.append('..')
from game_components.game_object_factory import ObjectFactory
from game_components.actors import *
from game_components.game_objects import *

class Initalizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initalize(self):
        pass

class FromStringInitalizer(Initalizer):
    def __init__(self, string) -> None:
        super().__init__()
        self.string = string

    def initalize(self, world) -> None:
        factory = ObjectFactory()
        commands = self.string.split('\n')
        for command in commands:
            command = command.split(' ')
            if command[0] == '//': continue
            obj_class = command[0]
            obj_args = command[1:]
            if 'chase' in obj_args:
                obj_args.append(world.mario)
            obj = factory.create(obj_class, obj_args)
            if obj_class == Mario.__name__:
                world.mario = obj
            if isinstance(obj, Actor):
                world.add_actor(obj)
            elif isinstance(obj, Ground):
                world.add_ground(obj)
            elif isinstance(obj, GameObject):
                world.add_object(obj)
        

class RefrenceFromStringInitalizer(Initalizer):
    def __init__(self, string) -> None:
        self.string = string
        self.x_ref = 0
        self.y_ref = 0

    def initalize(self, world) -> None:
        factory = ObjectFactory()
        commands = self.string.split('\n')
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