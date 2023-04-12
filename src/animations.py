import random
import pygame as pg
from .constants import Direction, GAME_WIDTH, GAME_HEIGHT
from .helpers import clamp, render_text


class DoomTile(pg.sprite.Sprite):
    TILE_WIDTH = 16
    TILE_HEIGHT = 32

    def __init__(self):
        self.color_pallete = [(0, 0, 0)] * 32
        for i in range(8):
            color_i = clamp(i * 32, 0, 255)
            # self.color_pallete[i + 0] = (0, 0, 0)
            # self.color_pallete[i + 8] = (255, color_i, 0)
            # self.color_pallete[i + 16] = (255, 255, color_i)
            # self.color_pallete[i + 24] = (0, 0, 0)
            self.color_pallete[i + 0] = (254, 107, 86)
            self.color_pallete[i + 8] = (255, 160, 104)
            self.color_pallete[i + 16] = (255, 209, 152)
            self.color_pallete[i + 24] = (255, 160, 104)
        self.fire_pixels = [[0 for _ in range(self.TILE_HEIGHT)]
                            for _ in range(self.TILE_WIDTH)]
        for x in range(self.TILE_WIDTH):
            self.fire_pixels[x][-1] = len(self.color_pallete) - 1
        self.update_fire_surface()

    def update_fire_effect(self):
        new_fire_pixels = [row.copy() for row in self.fire_pixels]

        for x in range(self.TILE_WIDTH):
            for y in range(1, self.TILE_HEIGHT):
                src_y = y + 1
                if src_y >= self.TILE_HEIGHT:
                    continue

                decay = random.randint(0, 4)
                new_x = (x - decay + self.TILE_WIDTH) % self.TILE_WIDTH
                new_intensity = max(self.fire_pixels[x][src_y] - decay, 0)

                new_fire_pixels[new_x][y] = new_intensity

        self.fire_pixels = new_fire_pixels
        self.update_fire_surface()

    def update_fire_surface(self):
        self.fire_surface = pg.Surface(
            (self.TILE_WIDTH, self.TILE_HEIGHT), pg.SRCALPHA)
        # Set the background color to transparent
        self.fire_surface.fill((255, 255, 255, 0))
        blank_coords = [(0, self.TILE_HEIGHT-1),
                        (self.TILE_WIDTH-1, self.TILE_HEIGHT-1)]
        for x in range(self.TILE_WIDTH):
            for y in range(self.TILE_HEIGHT):
                if (x, y) in blank_coords:
                    self.fire_surface.set_at((x, y), (0, 0, 0, 0))
                else:
                    intensity = self.fire_pixels[x][y]
                    if intensity > 0:  # Only update pixels with color
                        color = self.color_pallete[intensity]
                        self.fire_surface.set_at((x, y), color)

    def render_fire_effect(self, surface, x, y):
        surface.blit(self.fire_surface, (x, y))


class Fader:
    def __init__(self, dir: Direction = Direction.OUT):
        self.alpha = 0 if dir == Direction.OUT else 255
        self.direction = dir
        self.active = False
        self.speed = 8

    # FADING TO BLACK - DIRECTION IS OUT
    # START AT ALPHA 0 IS TRANSPARENT START AT 0
    # END AT BLACK ALPHA = 255

    def update(self):
        if self.active:
            if self.dir == Direction.OUT:
                if self.alpha > 255:
                    self.activate(Direction.IN)
                    return
                else:
                    self.alpha += self.speed * 2
            elif self.dir == Direction.IN:
                if self.alpha <= 0:
                    self.active = False
                else:
                    self.alpha -= self.speed

    def draw(self):
        temp_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)
        alpha = self.alpha
        if not self.active:
            alpha = 0
        temp_surface.fill((0, 0, 0, clamp(alpha, 0, 255)))
        return temp_surface

    def activate(self, dir, speed=8):
        self.active = True
        self.dir = dir
        self.alpha = 0 if dir == Direction.OUT else 255
        self.speed = speed


class TextBox:
    def __init__(self, messages, background_color=(0, 0, 0, 180), font_size=6, speed=75):
        self.background_color = background_color
        self.messages = messages
        self.current_message = 0
        self.current_character = 0
        self.font_size = font_size
        self.paused = False
        self.timer = 0
        self.speed = speed
        self.active = False
        self.text_box_image = pg.image.load(
            "resources/images/text_box_new.png").convert_alpha()
        self.text_box_image = pg.transform.scale(
            self.text_box_image, (GAME_WIDTH, GAME_HEIGHT//4))
        self.button_sprite = pg.image.load(
            "resources/sprites/a_button.png").convert_alpha()
        self.blink_timer = 0
        self.blink_frequency = 1000  # Time in milliseconds for each blink

    def start(self):
        self.active = True

    def next(self):
        if not self.paused:
            if self.current_character < len(self.messages[self.current_message]):
                self.current_character += 1
            else:
                self.paused = True

    def skip_to_end(self):
        self.current_character = len(self.messages[self.current_message])
        self.paused = True

    def advance_message(self):
        if self.active and self.current_message + 1 < len(self.messages):
            self.current_message += 1
            self.current_character = 0
        else:
            self.active = False

    def reset(self):
        self.current_message = 0
        self.current_character = 0

    def update(self, dt):
        if not self.active:
            return

        self.timer += dt
        if self.timer > self.speed:
            self.next()
            self.timer = 0
        self.blink_timer += dt
        if self.blink_timer >= self.blink_frequency:
            self.blink_timer = 0

    def draw(self):
        temp_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)
        self.text_box_image = pg.image.load(
            "resources/images/text_box_new.png").convert_alpha()
        self.text_box_image = pg.transform.scale(
            self.text_box_image, (GAME_WIDTH, GAME_HEIGHT//4))

        message = self.messages[self.current_message][:self.current_character]
        words = message.split(' ')

        lines = []
        current_line = ""
        accumulated_characters = 0

        for word in words:
            test_line = current_line + word + " "
            test_surface = render_text(
                test_line, self.font_size, color=(255, 255, 255))
            test_width = test_surface.get_width()

            if test_width > (256 - 40):  # available space in the textbox
                lines.append(current_line.strip())
                current_line = word + " "
                accumulated_characters += len(current_line)
            else:
                if accumulated_characters + len(word) <= self.current_character:
                    current_line += word + " "
                    accumulated_characters += len(word) + 1

        lines.append(current_line.strip())  # Add the last line

        for i, line in enumerate(lines):
            line_surface = render_text(
                line, self.font_size, color=(255, 255, 255))
            self.text_box_image.blit(line_surface, (20, 16 + i * 20))

        if self.paused and self.blink_timer < self.blink_frequency // 2:
            self.text_box_image.blit(
                self.button_sprite, (GAME_WIDTH - (32), 40))

        temp_surface.blit(self.text_box_image, (0, 3 * GAME_HEIGHT//4))

        return temp_surface
