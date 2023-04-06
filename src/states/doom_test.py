import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH
import random


class DoomTile:
    def __init__(self):
        self.color_pallete = [(0, 0, 0)] * 32
        for i in range(8):
            self.color_pallete[i + 0] = (i * 32, 0, 0)
            self.color_pallete[i + 8] = (255, i * 32, 0)
            self.color_pallete[i + 16] = (255, 255, i * 32)
            self.color_pallete[i + 24] = (255, 255, 255)
        self.scale = 1  # Adjust this value to control the resolution of the fire effect
        self.tile_width = 16
        self.tile_height = 32
        self.fire_pixels = [[0 for _ in range(self.tile_height)]
                            for _ in range(self.tile_width)]
        for x in range(self.tile_width):
            self.fire_pixels[x][-1] = len(self.color_pallete) - 1

    def update_fire_effect(self):
        tile_width = len(self.fire_pixels)
        tile_height = len(self.fire_pixels[0])
        new_fire_pixels = [row.copy() for row in self.fire_pixels]

        for x in range(tile_width):
            for y in range(1, tile_height):
                src_y = y + 1
                if src_y >= tile_height:
                    continue

                decay = random.randint(0, 3)
                new_x = (x - decay + tile_width) % tile_width
                new_intensity = max(self.fire_pixels[x][src_y] - decay, 0)

                new_fire_pixels[new_x][y] = new_intensity

        self.fire_pixels = new_fire_pixels

    def render_fire_effect(self, surface):
        tile_width = len(self.fire_pixels)
        tile_height = len(self.fire_pixels[0])
        for x in range(tile_width):
            for y in range(tile_height):
                intensity = self.fire_pixels[x][y]
                color = self.color_pallete[intensity]
                pg.draw.rect(surface, color, (self.x + x,
                             self.y + y, 1, 1))


class DoomTest(GameState):
    def __init__(self):
        super(DoomTest, self).__init__()
        self.next_state = "SPLASH"
        # Change x and y as needed
        self.layer1 = [DoomTile(x=i, y=0) for i in range(0, 320, 16)]
        self.layer2 = [DoomTile(x=i, y=32) for i in range(0, 320, 32)]
        self.fire_tiles = self.layer1 + self.layer2

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return

    def update(self, dt):
        for t in self.fire_tiles:
            t.update_fire_effect()

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT)).convert_alpha()
        surf.fill(255, 255, 255, 255)
        for i, t in enumerate(self.fire_tiles):
            t.render_fire_effect(surf)

        sidebar_width = (INFO.current_w - INFO.current_h) // 2
        scaled_win = pg.transform.scale(surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
