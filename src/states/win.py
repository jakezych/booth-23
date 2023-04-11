import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH, START_BUTTON
from ..helpers import render_text


class WinScreen(GameState):
    def __init__(self, duration=5000):
        super(WinScreen, self).__init__()
        self.next_state = "HOSPITAL"
        self.bottom_text = render_text("YOU WIN!", 8)
        self.bottom_text_rect = self.bottom_text.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT // 2))
        self.time_left = duration

    def update(self, dt):
        self.time_left -= dt
        if self.time_left < 0:
            self.done = True

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT)).convert()

        surf.blit(self.bottom_text, self.bottom_text_rect)

        sidebar_width = (INFO.current_w - INFO.current_h)//2
        scaled_win = pg.transform.scale(
            surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
