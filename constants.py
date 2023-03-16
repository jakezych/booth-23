from enum import Enum
import pygame

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

WIDTH = 320
HEIGHT = 320
FPS = 50
GRIDSIZE = 16
SCREEN_SCALING_FACTOR = 3.5
ANIM_SPEED = 3
TITLE_SCREEN_TIME = 25

obstacles = pygame.sprite.Group()
lights = pygame.sprite.Group()


DEATH_EVENT = pygame.event.custom_type()
WIN_EVENT = pygame.event.custom_type()
SHOW_MASKS = pygame.event.custom_type()


class Direction(Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4


class BlockType(Enum):
    COLLIDE = 0
    DEATH = 1
    WIN = 2
    LIGHT = 3
