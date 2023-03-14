from enum import Enum
import pygame


WIDTH = 320
HEIGHT = 320
FPS = 32
GRIDSIZE = 16
SCREEN_SCALING_FACTOR = 3

BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255,255,255)

obstacles = pygame.sprite.Group()

class Direction(Enum):
  UP = 1
  RIGHT = 2
  LEFT = 3
  DOWN = 4
