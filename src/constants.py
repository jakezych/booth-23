from enum import Enum
import pygame as pg

pg.init()
pg.joystick.init()
try:
    CONTROLLER = pg.joystick.Joystick(0)
except:
    CONTROLLER = None
FULLSCREEN = True

GAME_WIDTH = 256
GAME_HEIGHT = 256

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
cars: pg.sprite.Group = pg.sprite.Group()
car_spawners: pg.sprite.Group = pg.sprite.Group()


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
    "Eleven: Hopper??? Is that you? I can hear you in my head...",
    "Hopper's Voice: Eleven, it's me. You need to escape the Hawkins Lab.",
    "Eleven: ...",
    "Hopper's Voice: Find the portal to the Upside Down. It's your only way out.",
    "Hopper's Voice: Once you're there, retrieve the Eggo waffles. They hold a key to your power.",
    "Hopper's Voice: Be careful, the Demogorgon is lurking. It will try to stop you.",
    "Eleven: ...",
    "Hopper's Voice: Trust your instincts and your powers. I believe in you, kid.",
    "Eleven: ..."]

GAME_FONT_8 = pg.font.Font('./resources/fonts/font.ttf', 8)
GAME_FONT_10 = pg.font.Font('./resources/fonts/font.ttf', 10)

A_BUTTON = 1
B_BUTTON = 2
SELECT_BUTTON = 8
START_BUTTON = 9


INFO = pg.display.Info()
if FULLSCREEN:
    screen = pg.display.set_mode(
        (INFO.current_w, INFO.current_h-50), pg.FULLSCREEN)
else:
    screen = pg.display.set_mode(
        (INFO.current_w, INFO.current_h-50))
pg.display.set_caption(WINDOW_CAPTION)
