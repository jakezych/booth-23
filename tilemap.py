import pytmx
import pygame 
from constants import WIDTH, HEIGHT
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.util_pygame.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface
    

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_offset(self, entity, x_off, y_off):
        x,y = self.camera.topleft
        x += x_off
        y += y_off
        return entity.rect.move((x,y))

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        #set x and y position of camera
        #print(target.rect.centerx," ", int(WIDTH / 2))
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom
        #print(x,y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

pygame.quit()