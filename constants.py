import pygame
from enum import Enum

WIDTH = 640    
HEIGHT = 640
FPS = 6
GRIDSIZE = 16

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