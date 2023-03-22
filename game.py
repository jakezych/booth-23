import pygame
import tilemap
import sprites
import constants
import sys
from typing import Tuple
import media
import random
import animations


def get_maps() -> list[tilemap.GameMap]:
    first = tilemap.GameMap("data/maps/first/first.tmx", 0, None)
    second = tilemap.GameMap("data/maps/second/second.tmx", 0, None)
    third = tilemap.GameMap("data/maps/level1/level1.tmx", 0, None)
    #hospital = tilemap.TiledMap("data/maps/hospital/hospital.tmx", 0, None)
    #forest = tilemap.TiledMap("data/maps/forest/forest.tmx", 0, None)
    return [first, second, third]


def load_map(tm: tilemap.GameMap) -> sprites.Player:
    player = None
    for obj in tm.tmxdata.objects:
        if obj.name == 'player_spawn':
            player = sprites.Player(None, obj.x, obj.y, obj.x, obj.y)
        if obj.name == 'player_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, constants.BlockType.COLLIDE)
        if obj.name == 'death_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, constants.BlockType.DEATH)
        if obj.name == 'win_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, constants.BlockType.WIN)
        if obj.name == 'scare_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, constants.BlockType.SCARE)
        if obj.name == 'light':
            _ = sprites.Light(obj.x, obj.y, obj.width,
                              obj.height)
    return player


class Game:
    def __init__(self, screen_width, screen_height) -> None:
        self.maps = get_maps()
        self.screen_w, self.screen_h = screen_width, screen_height
        self.active_map = 0
        self.game_map = self.maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(self.game_map.width, self.game_map.height)
        self.show_masks = False
        self.timer = 0
        self.show_timer = True
        self.show_deaths = True
        self.done = False
        self.fader = animations.Fader()
        self.fader.activate(dir=constants.Direction.IN)
        self.deaths = 0

    def process_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == constants.DEATH_EVENT:
                self.deaths += 1
                self.player.grid_x = self.player.spawn_x
                self.player.grid_y = self.player.spawn_y
                self.player.dir = constants.Direction.UP
                self.player.anim_step = 0
                self.fader.activate(constants.Direction.IN)
                #self.player.title_screen = True
            elif event.type == constants.WIN_EVENT:
                self.change_map()
            elif event.type == constants.SHOW_MASKS_EVENT:
                self.show_masks = not self.show_masks
            elif event.type == constants.SHOW_TIMER_EVENT:
                self.show_timer = not self.show_timer

    def update_sprites(self) -> None:
        self.timer += 1
        self.player.update()
        self.camera.update(self.player)
        self.fader.update()

    def change_map(self) -> None:
        pygame.sprite.Group.empty(constants.obstacles)
        pygame.sprite.Group.empty(constants.lights)
        self.active_map = (self.active_map + 1) % len(self.maps)
        self.game_map = self.maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(
            self.game_map.width, self.game_map.height)
        self.player.scare = False
        self.player.scare_on_next = False
        self.player.show_title_screen = False
        self.fader.activate(constants.Direction.IN)

    def render_lights(self) -> None:
        # Blit lighting filter (should actually be after??)
        media.LIGHT_FILTER.fill(pygame.color.Color('white'))
        # -192 shifts center of light to center of player sprite
        media.LIGHT_FILTER.blit(
            # more negative is closer to top left
            media.PLAYER_5, self.camera.apply_offset(self.player, -(2*192), -(2*192)))
        for l in pygame.sprite.Group.sprites(constants.lights):
            media.LIGHT_FILTER.blit(
                media.PLAYER_5, self.camera.apply_offset(l, -2*192, -2*192))
        return media.LIGHT_FILTER

    def render_masks(self, temp_surface: pygame.Surface) -> pygame.Surface:

        # -- Uncomment to draw mask around player --
        # outline = [(p[0] + self.camera.apply(self.player)[0], p[1] +
        #            self.camera.apply(self.player)[1]) for p in self.player.mask.outline()]
        #pygame.draw.lines(temp_surface, (255, 0, 0), False, outline, 1)

        for block in filter(lambda x: x.type == sprites.BlockType.DEATH, constants.obstacles):
            outline = [(p[0] + self.camera.apply(block)[0], p[1] +
                        self.camera.apply(block)[1]) for p in block.mask.outline()]
            pygame.draw.lines(temp_surface, (255, 0, 0), False, outline, 1)
            overlap_mask = self.player.mask.overlap_mask(
                block.mask, (block.rect.x - self.player.grid_x, block.rect.y - self.player.grid_y))
            # -- Uncomment to draw overlap mask --
            # print(self.player.mask.overlap(block.mask, (block.rect.x -
            #      self.player.grid_x, block.rect.y - self.player.grid_y)))
            temp_surface.blit(overlap_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 255)),
                              self.camera.apply(self.player))
        return temp_surface

    def render_num(self, time: int, prefix: str = '', suffix: str = '') -> pygame.Surface:
        font = pygame.font.SysFont('arial', 15)
        font.set_bold(True)
        text = prefix + str(time) + suffix
        rendered = font.render(
            text, False, (255, 0, 0))
        return rendered

    def render_map(self) -> None:
        temp_surface = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        bottom_layer = self.game_map.draw_layer(None)
        temp_surface.blit(bottom_layer, self.camera.apply_rect(
            bottom_layer.get_rect()))
        temp_surface.blit(self.player.image, self.camera.apply(self.player))
        if self.show_masks:
            temp_surface = self.render_masks(temp_surface)
        top_layer = self.game_map.draw_layer('treetop')
        top_layer.set_colorkey((0, 0, 0))
        temp_surface.blit(top_layer,
                          self.camera.apply_rect(top_layer.get_rect()))
        return temp_surface

    def render_game(self, surf: pygame.Surface) -> Tuple[pygame.Surface, Tuple[int, int]]:
        # If need to render scare screen
        if self.player.scare:
            if self.done == False:
                pygame.mixer.music.load(media.SCARE_ROAR)
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                self.done = True
            return self.scare(), (0, 0)
        # Otws
        surf.blit(self.render_map(), (0, 0))
        surf.blit(self.render_lights(), (0, 0),
                  special_flags=pygame.BLEND_RGBA_SUB)

        if self.player.show_title_screen:
            surf.blit(media.TITLE_SCREEN_IMG, ((constants.WIDTH//2) -
                      (media.TITLE_SCREEN_IMG.get_width()//2), ((constants.HEIGHT//3) -
                      (media.TITLE_SCREEN_IMG.get_height()//2))))
        surf.blit(self.render_hud(), (0, 0))
        surf.blit(self.fader.draw(), (0, 0))

        pygame.transform.scale(
            surf, (self.screen_h, self.screen_h))

        sidebar_width = (self.screen_w - self.screen_h)//2

        scaled_win = pygame.transform.scale(
            surf, (self.screen_h, self.screen_h))

        return scaled_win, (sidebar_width, 0)

    def render_hud(self) -> None:
        temp_surface = pygame.Surface(
            (constants.WIDTH, constants.HEIGHT))
        # Render deaths:
        deaths_label = self.render_text("DEATHS")
        temp_surface.blit(deaths_label, (0, 25))
        deaths = self.render_text(str(self.deaths))
        temp_surface.blit(deaths, (0, deaths_label.get_height()+25))
        # Render
        level_label = self.render_text("LVL")
        level = self.render_text(str(self.active_map))
        temp_surface.blit(level_label, (constants.WIDTH//2 -
                                        (level_label.get_width()//2), 25))
        temp_surface.blit(level, (constants.WIDTH//2 -
                                  (level_label.get_width()//2), level_label.get_height() + 25))

        # Render
        timer = self.render_text(str(self.timer))
        if self.show_timer:
            time_label = self.render_text("TIME")
            temp_surface.blit(
                time_label, (constants.WIDTH - time_label.get_width(), 25))
            temp_surface.blit(timer, (constants.WIDTH -
                                      timer.get_width(), time_label.get_height() + 25))
        temp_surface.set_colorkey(constants.BLACK)
        return temp_surface

    def render_text(self, text: str) -> pygame.Surface:
        font = pygame.font.Font('data/font.ttf', 8)
        font.set_bold(False)
        font.set_italic(True)
        rendered = font.render(
            text, False, (255, 0, 0))
        return rendered

    def scare(self) -> pygame.Surface:
        scare = pygame.image.load(media.SCARE_IMG_PATH)
        surf = pygame.Surface(
            (self.screen_w, self.screen_h))
        surf.blit(scare, (0, 0))
        return surf
