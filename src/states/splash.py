import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH, START_BUTTON
from ..helpers import render_text
TITLE_SCREEN_PATH = "./resources/images/title.png"
LEVEL_MUSIC_PATH = "./resources/sounds/rbr_splatter.mp3"


class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = pg.transform.scale_by(
            pg.image.load(TITLE_SCREEN_PATH), 1.5)
        self.title_rect = self.title.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT//2 - 50))
        # self.next_state = "MAP1"
        # self.next_state = "MAP2"
        self.next_state = "HOSPITAL"
        # Add blinking text
        self.blinking_text = render_text("PRESS START", 10)
        self.blinking_text_rect = self.blinking_text.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT//2 + 50))
        self.blink_timer = 0
        self.blink_frequency = 1000  # Time in milliseconds for each blink

        self.bottom_text = render_text("© CMU CARNIVAL BOOTH 2023", 8)
        self.bottom_text_rect = self.bottom_text.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT - 40))

    def update(self, dt):
        self.blink_timer += dt
        if self.blink_timer >= self.blink_frequency:
            self.blink_timer = 0

    def startup(self, persistent):
        self.persist = persistent
        pg.mixer.music.load(LEVEL_MUSIC_PATH)
        pg.mixer.music.set_volume(0.25)
        pg.mixer.music.play(-1)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return
            if event.key == pg.K_RETURN:
                self.done = True
        elif event.type == pg.JOYBUTTONDOWN:
            if event.button == START_BUTTON:
                self.done = True

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT)).convert()
        surf.blit(self.title, self.title_rect)

        if self.blink_timer < self.blink_frequency // 2:
            surf.blit(self.blinking_text, self.blinking_text_rect)

        surf.blit(self.bottom_text, self.bottom_text_rect)

        sidebar_width = (INFO.current_w - INFO.current_h)//2
        scaled_win = pg.transform.scale(
            surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
