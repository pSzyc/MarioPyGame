import pygame
from actors import Mario, Ghost
from move import *
from itertools import combinations

GREEN = (34, 139, 34)

class ground:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def width(self):
        return self._width
    
    @property
    def height(self):
        return self._height

    @property
    def rectangle(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def grass(self):
        return pygame.Rect(self.x, self.y, self._width, 5)


    def draw(self, screen):
        # Draw the ground
        pygame.draw.rect(screen, (139, 69, 19), self.rectangle)
        pygame.draw.rect(screen, GREEN, self.grass())
        
class World:
    def __init__(self):
        self.actors = []
        self.mario = None
        self.screen = None
        self.ground_objects = []
        self._gravity = 1

    def initalize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.init_actors()
        self.init_ground()

    def init_ground(self):
        self.add_ground(ground(0, 500, 400, 100))
        self.add_ground(ground(400, 300, 400, 300))

    def init_actors(self):
        self.mario = Mario(50, 50, 0, 0, ControlMoveStrategy)
        self.add_actor(self.mario)
        self.add_actor(Ghost(500, 100, 5, 0, BackAndForthMoveStrategy))

    def add_ground(self, ground):
        self.ground_objects.append(ground)

    def add_actor(self, actor):
        self.actors.append(actor)

    def move_actors(self):
        for actor in self.actors:
            actor.move()
    
    def draw_actors(self):
        for actor in self.actors:
            actor.draw(self.screen)

    def handle_collision(self):
        for actor1, actor2 in combinations(self.actors, 2):
            if actor1.rectangle.colliderect(actor2.rectangle):
                actor1.handle_collision(actor2.rectangle)
                actor2.handle_collision(actor1.rectangle)

        for actor in self.actors:
            for ground in self.ground_objects:
                if actor.rectangle.colliderect(ground.rectangle):
                    actor.handle_collision(ground.rectangle)

    def gravity(self):
        for actor in self.actors:
            actor.gravity(self._gravity)

    def draw_gorund(self):
        for ground in self.ground_objects:
            ground.draw(self.screen)

    def draw(self):
        self.screen.fill((100, 100, 255))
        self.draw_actors()
        self.draw_gorund()
        pygame.display.update()