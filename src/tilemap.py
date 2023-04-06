import pytmx
import pygame
from . import constants


class TiledMap:
    def __init__(self, filename: str) -> None:
        tm = pytmx.util_pygame.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def blit_layer(self, surface, filter) -> None:
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if filter != None:
                if isinstance(layer, pytmx.TiledTileLayer) and layer.name == filter:
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))
            else:
                if isinstance(layer, pytmx.TiledTileLayer):
                    for x, y, gid, in layer:
                        tile = ti(gid)
                        if tile:
                            surface.blit(tile, (x * self.tmxdata.tilewidth,
                                                y * self.tmxdata.tileheight))

    def draw_layer(self, filter='treetop') -> pygame.Surface:
        temp_surface = pygame.Surface(
            (self.width, self.height), pygame.SRCALPHA)
        #temp_surface.fill((0, 0, 0, 0))
        self.blit_layer(temp_surface, filter)
        return temp_surface


class Camera:
    def __init__(self, width: int, height: int) -> None:
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity: pygame.sprite.Sprite) -> pygame.Rect:
        return entity.rect.move(self.camera.topleft)

    def apply_offset(self, entity: pygame.sprite.Sprite, x_off: int, y_off: int) -> pygame.Rect:
        x, y = self.camera.topleft
        x += x_off
        y += y_off
        return entity.rect.move((x, y))

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(self.camera.topleft)

    def update(self, target: pygame.sprite.Sprite) -> None:
        # set x and y position of camera
        #print(target.rect.centerx," ", int(WIDTH / 2))
        x = -target.rect.centerx + int(constants.GAME_WIDTH / 2)
        y = -target.rect.centery + int(constants.GAME_HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - constants.GAME_WIDTH), x)  # right
        y = max(-(self.height - constants.GAME_HEIGHT), y)  # bottom
        # print(x,y)
        self.camera = pygame.Rect(x, y, self.width, self.height)


class GameMap(TiledMap):
    def __init__(self, filename: str, level_id: int, desc_image: pygame.Surface) -> None:
        TiledMap.__init__(self, filename=filename)
        self.level_id = level_id
        self.image = desc_image

    def draw_description(self):
        return self.image
