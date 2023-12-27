from abc import abstractmethod
import pygame
from move import MoveStrategy
from objects import GameObject

class Actor(GameObject):
    def __init__(self, x, y, speed_x, speed_y, move_strategy, width, height, image):
        super().__init__(x, y, width, height, image)
        self._speed_x = speed_x
        self._speed_y = speed_y
        self.x_prev = x
        self.y_prev = y
        self._move_strategy = move_strategy
        self._facing_right = True

    @property
    def facing_right(self):
        return self._facing_right
    
    @facing_right.setter
    def facing_right(self, value):
        self._facing_right = value

    @property
    def prev_rectangle(self):
        return pygame.Rect(self.x_prev, self.y_prev, self.width, self.height)

    @property
    def move_strategy(self):
        return self._move_strategy
    
    @move_strategy.setter
    def move_strategy(self, move_strategy):
        self._move_strategy = move_strategy

    @property
    def speed_x(self):
        return self._speed_x
    
    @speed_x.setter
    def speed_x(self, value):
        self._speed_x = value

    @property
    def speed_y(self):
        return self._speed_y
    
    @speed_y.setter
    def speed_y(self, value):
        self._speed_y = value
    
    def gravity(self, gravity):
        self.speed_y += gravity
    
    @abstractmethod
    def on_turn(self, isRight):
        pass

    @abstractmethod
    def move(self):
        pass

class Ghost(Actor):
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, image, width=40, height=40):
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
    
    def on_turn(self, isRight):
        if self.facing_right != isRight:
            self.facing_right = not self.facing_right
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed_x = - self.speed_x

    def move(self):
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    def draw(self, screen, x_offset, y_offset):
        # Draw Mario image
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Mario(Actor):
    def __init__(self, x, y, speed_x, speed_y, move_strategy: MoveStrategy, image, width=40, height=60):
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
        self.speed = 7.5
        self.jump_energy = 0
        self.lifes = 3
        self.coins = 0
        self.stunned_time = 0

    def on_turn(self, isRight):
        if self.facing_right != isRight:
            self.facing_right = not self.facing_right
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed_x += 2 * (isRight - 0.5) * self.speed
        
        # clip speed
        if self.speed_x > self.speed:
            self.speed_x = self.speed
        elif self.speed_x < -self.speed:
            self.speed_x = -self.speed

    def draw(self, screen, x_offset, y_offset):
        # Draw Mario image
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)
        
        # Draw lifes as hearts in left upper corner
        heart_image = pygame.image.load("resources/heart.png")
        heart_width = 30
        heart_height = 30
        heart_image = pygame.transform.scale(heart_image, (heart_width, heart_height))
        for i in range(self.lifes):
            heart_rect = pygame.Rect(i * heart_width, 0, heart_width, heart_height)
            screen.blit(heart_image, heart_rect)
        
        # Draw number of coins in right upper corner
        font = pygame.font.Font(None, 35)
        coins_text = font.render(f"Coins: {self.coins}", True, (255, 255, 255))
        coins_rect = coins_text.get_rect()
        coins_rect.topright = (screen.get_width(), 0)
        screen.blit(coins_text, coins_rect)

    def jump(self):
        if self.jump_energy >= 20:
            self.speed_y -= self.jump_energy
            self.jump_energy = 0

    def move(self):
        if self.stunned_time == 0:
            if self.jump_energy < 20:
                self.jump_energy += 1
            x_new, y_new = self.move_strategy.propose_move(self)
        else:
            self.stunned_time -= 1
            x_new = self.x + self.speed_x
            y_new = self.y + self.speed_y

        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new