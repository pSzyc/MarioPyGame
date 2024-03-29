from abc import abstractmethod
import pygame
import sys
sys.path.append('..')
from game_logic.move import MoveStrategy
from game_components.game_objects import GameObject

class Actor(GameObject):
    __slots__ = ['_speed_x', '_speed_y', '_x_prev', '_y_prev', '_move_strategy', '_facing_right']
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, move_strategy: MoveStrategy, width: int, height: int, image: pygame.Surface) -> None:
        super().__init__(x, y, width, height, image)
        self._speed_x = speed_x
        self._speed_y = speed_y
        self._x_prev = x
        self._y_prev = y
        self._move_strategy = move_strategy
        self._facing_right = True

    @property
    def x_prev(self) -> int:
        return self._x_prev
    
    @x_prev.setter
    def x_prev(self, value: int) -> None:
        self._x_prev = value
    
    @property
    def y_prev(self) -> int:
        return self._y_prev
    
    @y_prev.setter
    def y_prev(self, value: int) -> None:
        self._y_prev = value

    @property
    def facing_right(self) -> bool:
        return self._facing_right
    
    @facing_right.setter
    def facing_right(self, value: bool) -> None:
        self._facing_right = value

    @property
    def prev_rectangle(self) -> pygame.Rect:
        return pygame.Rect(self.x_prev, self.y_prev, self.width, self.height)

    @property
    def move_strategy(self) -> MoveStrategy:
        return self._move_strategy
    
    @move_strategy.setter
    def move_strategy(self, move_strategy: MoveStrategy) -> None:
        self._move_strategy = move_strategy

    @property
    def speed_x(self) -> float:
        return self._speed_x

    @speed_x.setter
    def speed_x(self, value: float) -> None:
        self._speed_x = value

    @property
    def speed_y(self) -> float:
        return self._speed_y
    
    @speed_y.setter
    def speed_y(self, value: float) -> None:
        self._speed_y = value
    
    def gravity(self, gravity: float) -> None:
        self.speed_y += gravity
    
    @abstractmethod
    def on_turn(self, isRight: bool) -> None:
        pass

    @abstractmethod
    def move(self) -> None:
        pass

class Ghost(Actor):
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, move_strategy: MoveStrategy, image: pygame.Surface, width: int = 40, height: int = 40) -> None:
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
    
    def on_turn(self, isRight: bool) -> None:
        if self.facing_right != isRight:
            self.facing_right = not self.facing_right
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed_x = - self.speed_x

    def move(self) -> None:
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        # Draw Mario image
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)

class Mario(Actor):
    __slots__ = ['_speed', '_jump_energy', '_lifes', '_coins', '_stunned_time', '_isSleeping']
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, move_strategy: MoveStrategy, image: pygame.Surface, width: int = 40, height: int = 60) -> None:
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)
        self._speed = 7.5
        self._jump_energy = 0
        self._lifes = 3
        self._coins = 0
        self._stunned_time = 0
        self._isSleeping = False

    @property
    def jump_energy(self) -> int:
        return self._jump_energy
    
    @jump_energy.setter
    def jump_energy(self, value: int) -> None:
        self._jump_energy = value
        
    @property
    def lifes(self) -> int:
        return self._lifes
    
    @lifes.setter
    def lifes(self, value: int) -> None:
        self._lifes = value
    
    @property
    def coins(self) -> int:
        return self._coins
    
    @coins.setter
    def coins(self, value: int) -> None:
        self._coins = value

    @property
    def stunned_time(self) -> int:
        return self._stunned_time
    
    @stunned_time.setter
    def stunned_time(self, value: int) -> None:
        self._stunned_time = value

    @property
    def isSleeping(self) -> bool:
        return self._isSleeping
    
    @isSleeping.setter
    def isSleeping(self, value: bool) -> None: 
        self._isSleeping = value

    def on_turn(self, isRight: bool) -> None:
        if self.facing_right != isRight:
            self.facing_right = not self.facing_right
            self.image = pygame.transform.flip(self.image, True, False)
        self.speed_x += 2 * (isRight - 0.5) * self._speed
        
        # clip speed
        if self.speed_x > self._speed:
            self.speed_x = self._speed
        elif self.speed_x < -self._speed:
            self.speed_x = -self._speed

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int):
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

    def jump(self) -> None:
        if self.jump_energy >= 20:
            self.speed_y -= self.jump_energy
            self.jump_energy = 0

    def move(self) -> None:
        if self.stunned_time == 0:
            if self.isSleeping:
                self.wake_up()
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
    
    def fall_asleep(self) -> None:
        if not self.isSleeping:
            self.isSleeping = True
            self.image = pygame.transform.rotate(self.image, 90)
            self.width, self.height = self.height, self.width
    
    def wake_up(self) -> None:
        if self.isSleeping:
            self.isSleeping = False
            self.jump_energy = 0
            self.speed_y = -20
            self.image = pygame.transform.rotate(self.image, -90)
            self.width, self.height = self.height, self.width

class Bomb(Actor):
    def __init__(self, x: int, y: int, speed_x: float, speed_y: float, move_strategy: MoveStrategy, image: pygame.Surface, width: int = 40, height: int = 40) -> None:
        super().__init__(x, y, speed_x, speed_y, move_strategy, width, height, image)

    def on_turn(self, isRight: bool) -> None:
        if self.facing_right != isRight:
            self.facing_right = not self.facing_right
            self.image = pygame.transform.flip(self.image, True, False)
            self.speed_x = - self.speed_x

    def move(self) -> None:
        x_new, y_new = self.move_strategy.propose_move(self)
        self.x_prev = self.x
        self.y_prev = self.y
        self.x = x_new
        self.y = y_new

    def draw(self, screen: pygame.Surface, x_offset: int, y_offset: int) -> None:
        draw_rect = pygame.Rect(self.x - x_offset, self.y - y_offset, self.width, self.height)
        screen.blit(self.image, draw_rect)