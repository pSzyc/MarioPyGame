from actors_factory import ObjectFactory
from abc import ABC, abstractmethod
from actors import *
from objects import *
from ground import *

class Initalizer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def initalize(self):
        pass

class FromStringInitalizer(Initalizer):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def initalize(self, world):
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