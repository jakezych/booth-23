import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH, INFO

SCARE_IMAGE_PATH = "./resources/images/scare.png"
SCARE_ROAR_PATH = "./resources/sounds/scare.mp3"


class ScareScreen(GameState):
    def __init__(self):
        super(ScareScreen, self).__init__()
        self.next_state = "CREDITS"
        self.time_remaining = 2500
        self.scare_img = pg.image.load(SCARE_IMAGE_PATH)
        self.scare_img = pg.transform.scale(
            self.scare_img, (INFO.current_w, INFO.current_h))

    def startup(self, persistent):
        self.persist = persistent
        pg.mixer.music.load(SCARE_ROAR_PATH)
        pg.mixer.music.set_volume(1)
        pg.mixer.music.play()

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return

    def update(self, dt):
        self.time_remaining -= dt
        if self.time_remaining < 0:
            self.done = True

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((INFO.current_w, INFO.current_h)).convert()
        surf.blit(self.scare_img, (0, 0))
        surface.blit(surf, (0, 0))
