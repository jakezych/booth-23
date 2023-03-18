import pygame
import constants

# Visual
TITLE_SCREEN_PATH = 'data/sprites/title.png'
SCARE_IMG_PATH = 'data/sprites/scare.png'

TITLE_SCREEN_IMG = pygame.image.load(TITLE_SCREEN_PATH)
SCARE_IMG = pygame.image.load(SCARE_IMG_PATH)

# Audio
LEVEL_1_MUSIC = 'data/music/rbr_splatter.mp3'
SCARE_ROAR = 'data/music/scare.mp3'

# MISC
PLAYER_5 = pygame.transform.scale_by(
    pygame.image.load('data/spotlights/spotlight6.png'), 1)
LIGHT_FILTER = pygame.surface.Surface((constants.WIDTH, constants.HEIGHT))
