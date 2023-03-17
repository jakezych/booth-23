import pygame
import constants

PLAYER_5 = pygame.transform.scale_by(
    pygame.image.load('data/spotlights/spotlight6.png'), 1)
LIGHT_FILTER = pygame.surface.Surface((constants.WIDTH, constants.HEIGHT))
