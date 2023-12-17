import pygame
from actors import Mario

class World:
    def __init__(self):
        self.actors = []
        self.screen = None
        self.ground_objects = []

    def initalize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.init_actors()
        self.init_ground()

    def init_ground(self):
        ground_rect = pygame.Rect(0, 400, 800, 200)
        self.ground_objects.append(ground_rect)

    def init_actors(self):
        self.add_actor(Mario(50, 50))

    def add_actor(self, actor):
        self.actors.append(actor)

    def move_actors(self):
        for actor in self.actors:
            actor.move()
    
    def draw_actors(self):
        for actor in self.actors:
            actor.draw(self.screen)
    
    def handle_collision(self):
        for actor in self.actors:
            for ground in self.ground_objects:
                if actor.rect.colliderect(ground):
                    actor.handle_collision(ground)

    def draw_gorund(self):
        for ground in self.ground_objects:
            pygame.draw.rect(self.screen, (139, 69, 19), ground)

    def draw(self):
        self.screen.fill((100, 100, 255))
        self.draw_actors()
        self.draw_gorund()
        pygame.display.update()