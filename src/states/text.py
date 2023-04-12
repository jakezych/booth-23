import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH, Direction
from ..helpers import render_text
from .. import animations


FONT_PATH = "./resources/fonts/font.ttf"
TITLE_SCREEN_PATH = "./resources/images/title.png"
SCOTTY_PATH = "./resources/images/scotty.png"


class TextScreen(GameState):
    def __init__(self):
        super(TextScreen, self).__init__()
        self.next_state = "MAP3"
        self.time_remaining = 2500
        self.total_time = 2500
        self.text = "THE UPSIDE DOWN"
        self.font_size = 10
        self.reflect = False
        self.text = render_text("THE UPSIDE DOWN", self.font_size)
        self.text_rect = self.text.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT//2))
        self.fader = animations.Fader()

    def startup(self, persistent):
        self.persist = persistent
        self.fader.activate(dir=Direction.IN, speed=3)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return

    def update(self, dt):
        self.time_remaining -= dt
        if not self.reflect and self.time_remaining < self.total_time // 2:
            self.reflect = True
            # self.text = pg.transform.flip(self.text, False, True)
            self.text = pg.transform.rotate(self.text, 180)
        if self.time_remaining < 0:
            self.done = True
        self.fader.update()

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))

        surf.blit(self.text, self.text_rect)
        surf.blit(self.fader.draw(), (0, 0))

        sidebar_width = (INFO.current_w - INFO.current_h)//2
        scaled_win = pg.transform.scale(
            surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
