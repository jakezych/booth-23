from enum import Enum
import pygame as pg

pg.init()
FULLSCREEN = False

GAME_WIDTH = 320
GAME_HEIGHT = 320

WINDOW_CAPTION = 'Stranger Things ΦΔΘ'
# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

GRIDSIZE = 16
ANIM_SPEED = 3


obstacles: pg.sprite.Group = pg.sprite.Group()
lights: pg.sprite.Group = pg.sprite.Group()


DEATH_EVENT = pg.event.custom_type()
WIN_EVENT = pg.event.custom_type()
SHOW_MASKS_EVENT = pg.event.custom_type()
SHOW_TIMER_EVENT = pg.event.custom_type()
SCARE_EVENT = pg.event.custom_type()


class Direction(Enum):
    UP = 1
    RIGHT = 2
    LEFT = 3
    DOWN = 4
    OUT = 5
    IN = 6


class BlockType(Enum):
    COLLIDE = 0
    DEATH = 1
    WIN = 2
    LIGHT = 3
    SCARE = 4


MAP1_TEXT = [
    "Eleven! Wake up! Wake up!...",
    "Eleven: Hopper? Is that you? I can hear you in my mind...",
    "Hopper's Voice: Eleven, it's me. I'm communicating with you telepathically. ",
    "You need to escape the Hawkins Lab.",
    "Eleven: ...",
    "Hopper's Voice: Find the secret passage to the Upside Down. It's your only way out.",
    "Eleven: ...",
    "Hopper's Voice: Once you're there, retrieve the Eggo waffles. They hold a key to your power.",
    "Eleven: ...",
    "Hopper's Voice: Be careful, the Demogorgon is lurking. It will try to stop you.",
    "Eleven: ...",
    "Hopper's Voice: Trust your instincts and your powers. I believe in you, kid.",
    "Eleven: I will do my best, Hopper."]

GAME_FONT_8 = pg.font.Font('./resources/fonts/font.ttf', 8)
GAME_FONT_10 = pg.font.Font('./resources/fonts/font.ttf', 10)
