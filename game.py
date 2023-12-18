import pygame
import sys
from world import World

def check_for_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 

if __name__ == '__main__':
    world = World()
    world.initalize()
    clock = pygame.time.Clock()

    while True:
        check_for_quit()
        world.gravity()
        world.move_actors()
        world.handle_collision()
        world.draw()
        clock.tick(30)