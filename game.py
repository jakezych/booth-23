import pygame
import tilemap
import sprites
import constants
import sys
from typing import Tuple
import media


def get_maps() -> list[tilemap.TiledMap]:
    first = tilemap.TiledMap("data/maps/first/first.tmx")
    second = tilemap.TiledMap("data/maps/second/second.tmx")
    title_map = tilemap.TiledMap("data/maps/level1/level1.tmx")
    #wood_map = tilemap.TiledMap("data/maps/title_map/title_map.tmx")
    return [first, second, title_map][::-1]


def load_map(tm: tilemap.TiledMap) -> sprites.Player:
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
        self.screen_w = screen_width
        self.screen_h = screen_height
        self.active_map = 0
        self.game_map = self.maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(self.game_map.width, self.game_map.height)
        self.show_masks = False
        self.done = False

    def process_events(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == constants.DEATH_EVENT:
                self.player.grid_x = self.player.spawn_x
                self.player.grid_y = self.player.spawn_y
                self.player.dir = constants.Direction.UP
                self.player.anim_step = 0
                #self.player.title_screen = True
            elif event.type == constants.WIN_EVENT:
                self.change_map()
            elif event.type == constants.SHOW_MASKS_EVENT:
                self.show_masks = not self.show_masks

    def update_sprites(self) -> None:
        self.player.update()
        self.camera.update(self.player)

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

    def render_lights(self) -> None:
        # Blit lighting filter (should actually be after??)
        media.LIGHT_FILTER.fill(pygame.color.Color('white'))
        # -192 shifts center of light to center of player sprite
        media.LIGHT_FILTER.blit(
            # more negative is closer to top left
            media.PLAYER_5, self.camera.apply_offset(self.player, -(192), -(192)))
        for l in pygame.sprite.Group.sprites(constants.lights):
            media.LIGHT_FILTER.blit(
                media.PLAYER_5, self.camera.apply_offset(l, -192, -192))
        return media.LIGHT_FILTER

    def render_masks(self, temp_surface: pygame.Surface) -> pygame.Surface:

        # outline = [(p[0] + self.camera.apply(self.player)[0], p[1] +
        #            self.camera.apply(self.player)[1]) for p in self.player.mask.outline()]
        #pygame.draw.lines(temp_surface, (255, 0, 0), False, outline, 1)

        for block in filter(lambda x: x.type == sprites.BlockType.DEATH, constants.obstacles):
            outline = [(p[0] + self.camera.apply(block)[0], p[1] +
                        self.camera.apply(block)[1]) for p in block.mask.outline()]
            pygame.draw.lines(temp_surface, (255, 0, 0), False, outline, 1)
            overlap_mask = self.player.mask.overlap_mask(
                block.mask, (block.rect.x - self.player.grid_x, block.rect.y - self.player.grid_y))
            # print(self.player.mask.overlap(block.mask, (block.rect.x -
            #      self.player.grid_x, block.rect.y - self.player.grid_y)))
            temp_surface.blit(overlap_mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 0, 0, 255)),
                              self.camera.apply(self.player))
        return temp_surface

    def render_map(self) -> None:
        map_img_bot = self.game_map.make_map()
        map_img_top = self.game_map.make_map_top()
        map_img_top.set_colorkey((0, 0, 0))
        map_rect = map_img_bot.get_rect()
        temp_surface = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        # Blit game elements onto the window
        temp_surface.blit(map_img_bot, self.camera.apply_rect(map_rect))
        temp_surface.blit(self.player.image, self.camera.apply(self.player))
        if self.show_masks:
            temp_surface = self.render_masks(temp_surface)
        temp_surface.blit(map_img_top, self.camera.apply_rect(map_rect))
        return temp_surface

    def render_game(self, surf: pygame.Surface) -> Tuple[pygame.Surface, Tuple[int, int]]:
        if self.player.scare:
            if self.done == False:
                pygame.mixer.music.load(media.SCARE_ROAR)
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                self.done = True
            return self.scare(), (0, 0)
        surf.blit(self.render_map(), (0, 0))
        surf.blit(self.render_lights(), (0, 0),
                  special_flags=pygame.BLEND_RGBA_SUB)
        if self.player.title_screen:
            surf.blit(media.TITLE_SCREEN_IMG, (77, 25))
        scaled_win = pygame.transform.scale(surf, (
            constants.WIDTH*constants.SCREEN_SCALING_FACTOR, constants.HEIGHT*constants.SCREEN_SCALING_FACTOR))
        return scaled_win, (340, 0)

    def scare(self) -> pygame.Surface:
        scare = pygame.image.load(media.SCARE_IMG_PATH)
        surf = pygame.Surface(
            (self.screen_w, self.screen_h))
        surf.blit(scare, (0, 0))
        return surf
