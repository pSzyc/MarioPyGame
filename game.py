#!/usr/bin/python3
import pygame
import sys
from utilities.initalize import RefrenceFromFileInitalizer
from game_logic.game_manager import GameManager
import time
from game_components.world import World

def end_game():
    time.sleep(3)
    pygame.quit()
    sys.exit()

def draw_message(world: World, message: str) -> None:
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (255, 255, 255))
    text_rect = text.get_rect(center=(world.screen.get_width() // 2, world.screen.get_height() // 2))
    world.screen.blit(text, text_rect)
    pygame.display.update()

def check_for_quit() -> None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() 

if __name__ == '__main__':
    world = RefrenceFromFileInitalizer('resources/board.txt').initalize()
    game_manager = GameManager(world)
    clock = pygame.time.Clock()
    while True:
        check_for_quit()
        outcome = game_manager.step()
        clock.tick(30)
        if outcome == 'Lose':
            draw_message(world, "You lose")
            end_game()
        elif outcome == 'Win':
            draw_message(world, 'You win')
            end_game()
