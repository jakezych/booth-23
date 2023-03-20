import pygame
from constants import *

FADE_SPEED = 8


class Fader:
    def __init__(self, dir: Direction = Direction.OUT):
        self.alpha = 0 if dir == Direction.OUT else 255
        self.direction = dir
        self.active = False

    # FADING TO BLACK - DIRECTION IS OUT
    # START AT ALPHA 0 IS TRANSPARENT START AT 0
    # END AT BLACK ALPHA = 255

    def update(self):
        if self.active:
            if self.dir == Direction.OUT:
                if self.alpha > 255:
                    self.activate(Direction.IN)
                    return
                else:
                    self.alpha += FADE_SPEED * 2
            elif self.dir == Direction.IN:
                if self.alpha < 0:
                    self.active = False
                else:
                    self.alpha -= FADE_SPEED

    def draw(self):
        temp_surface = pygame.Surface((WIDTH, HEIGHT))
        temp_surface.fill(BLACK)
        alpha = self.alpha
        if not self.active:
            alpha = 0
        temp_surface.fill(BLACK)
        temp_surface.set_alpha(alpha)
        return temp_surface

    def activate(self, dir):
        self.active = True
        self.dir = dir
        self.alpha = 0 if dir == Direction.OUT else 255
