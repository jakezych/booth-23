import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH

FONT_PATH = "./resources/fonts/font.ttf"
TITLE_SCREEN_PATH = "./resources/images/title.png"


class CreditScreen(GameState):
    def __init__(self):
        super(CreditScreen, self).__init__()
        self.next_state = "SPLASH"
        self.time_remaining = 60
        self.credits_list = [
            "Created By:",
            "Victor Alfonzo",
            "Jake Zych",
            "",
            "Special Thanks:",
            "Mukundh Balajee",
            "Jaime Romero",
            "Pranav Addepalli",
            "Lake Lewis",
            "Yoona Lee",
            "Jack Troy",
            "Michael Sun",
            "",
            "On behalf of",
            "Phi Delta Theta",
            "PA Rho",
            "",
            "Have a great carnival!",

        ]
        self.y_offset = 80
        self.scroll_speed = 0.5
        self.font_size = 12
        self.title = pg.transform.scale_by(
            pg.image.load(TITLE_SCREEN_PATH), 1.5)

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return

    def update(self, dt):
        self.y_offset += self.scroll_speed
        if self.y_offset > 700:
            self.y_offset = 0
            self.done = True
            self.persist["deaths"] = 0
            self.persist["timer"] = 0

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT))
        font = pg.font.FontType(FONT_PATH, self.font_size)
        title_rect = self.title.get_rect(
            center=(GAME_WIDTH//2, GAME_HEIGHT - self.y_offset - (6 * self.title.get_height()//8)))
        surf.blit(self.title, title_rect)
        for i, line in enumerate(self.credits_list):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(
                center=(GAME_WIDTH // 2, GAME_HEIGHT - self.y_offset + i * self.font_size * 1.5))
            surf.blit(text_surface, text_rect)

        sidebar_width = (INFO.current_w - INFO.current_h)//2
        scaled_win = pg.transform.scale(
            surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
