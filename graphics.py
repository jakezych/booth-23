import pygame
import constants

PLAYER_5 = pygame.transform.scale_by(
    pygame.image.load('data/spotlights/spotlight5.png'), 0.75)
LIGHT_FILTER = pygame.surface.Surface((constants.WIDTH, constants.HEIGHT))
