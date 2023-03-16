
import sys
import pygame
import constants
import sprites
import tilemap


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
    return player


class Game:
    def __init__(self, maps):
        self.maps = maps
        self.active_map = 0
        self.game_map = maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(self.game_map.width, self.game_map.height)

    def process_events(self):
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

    def update_sprites(self):
        self.player.update()
        self.camera.update(self.player)

    def change_map(self):
        self.active_map = (self.active_map + 1) % len(self.maps)
        self.game_map = self.maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(
            self.game_map.width, self.game_map.height)


def get_maps():
    title_map = tilemap.TiledMap("data/maps/level1/level1.tmx")
    wood_map = tilemap.TiledMap("data/maps/title_map/title_map.tmx")
    return [title_map, wood_map]


def main():
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('PDT Booth23')
    size = width, height = constants.WIDTH, constants.HEIGHT

    light = pygame.transform.scale_by(
        pygame.image.load('data/spotlights/spotlight5.png'), 0.75)
    light_filter = pygame.surface.Surface(size)

    title = pygame.image.load('data/sprites/title.png')

    window = pygame.Surface(size)
    screen = pygame.display.set_mode(
        (width*constants.SCREEN_SCALING_FACTOR, height*constants.SCREEN_SCALING_FACTOR))

    game = Game(get_maps())

    while True:
        game.process_events()
        game.update_sprites()

        map_img_bot = game.game_map.make_map()
        map_img_top = game.game_map.make_map_top()
        map_img_top.set_colorkey((0, 0, 0))
        map_rect = map_img_bot.get_rect()

        # Blit lighting filter (should actually be after??)
        light_filter.fill(pygame.color.Color('white'))
        # -42 shifts center of light to center of player sprite
        light_filter.blit(
            light, game.camera.apply_offset(game.player, -66, -66))

        # Blit game elements onto the window
        window.blit(map_img_bot, game.camera.apply_rect(map_rect))
        # win.blit(dg.image, camera.apply(dg))
        window.blit(game.player.image, game.camera.apply(game.player))
        window.blit(map_img_top, game.camera.apply_rect(map_rect))
        window.blit(light_filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
        if game.player.title_screen:
            window.blit(title, (77, 50))
        # Scale the window to the screen size
        scaled_win = pygame.transform.scale(window, screen.get_size())
        screen.blit(scaled_win, (0, 0))
        clock.tick(constants.FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()
