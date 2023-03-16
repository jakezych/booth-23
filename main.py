
import sys
import pygame
import constants
import sprites
import tilemap
import graphics


def get_maps() -> list[tilemap.TiledMap]:
    title_map = tilemap.TiledMap("data/maps/level1/level1.tmx")
    wood_map = tilemap.TiledMap("data/maps/title_map/title_map.tmx")
    return [title_map, wood_map][::-1]
    # return [title_map, wood_map]


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
        if obj.name == 'light':
            _ = sprites.Light(obj.x, obj.y, obj.width,
                              obj.height)
    return player


class Game:
    def __init__(self, maps: list[tilemap.TiledMap] = None) -> None:
        self.maps = get_maps() if maps is None else maps
        self.active_map = 0
        self.game_map = self.maps[self.active_map]
        self.player = load_map(self.game_map)
        self.camera = tilemap.Camera(self.game_map.width, self.game_map.height)
        self.show_masks = False

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
            elif event.type == constants.SHOW_MASKS:
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

    def render_lights(self) -> None:
        # Blit lighting filter (should actually be after??)
        graphics.LIGHT_FILTER.fill(pygame.color.Color('white'))
        # -42 shifts center of light to center of player sprite
        graphics.LIGHT_FILTER.blit(
            graphics.PLAYER_5, self.camera.apply_offset(self.player, -68, -67))
        for l in pygame.sprite.Group.sprites(constants.lights):
            graphics.LIGHT_FILTER.blit(
                graphics.PLAYER_5, self.camera.apply_offset(l, -68, -67))
        return graphics.LIGHT_FILTER

    def render_masks(self, temp_surface: pygame.Surface) -> pygame.Surface:

        outline = [(p[0] + self.camera.apply(self.player)[0], p[1] +
                    self.camera.apply(self.player)[1]) for p in self.player.mask.outline()]
        pygame.draw.lines(temp_surface, (255, 0, 255), False, outline, 1)

        for block in constants.obstacles:
            outline = [(p[0] + self.camera.apply(block)[0], p[1] +
                        self.camera.apply(block)[1]) for p in block.mask.outline()]
            pygame.draw.lines(temp_surface, (255, 0, 255), False, outline, 1)
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


def main() -> None:
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('PDT Booth23')
    size = width, height = constants.WIDTH, constants.HEIGHT
    title = pygame.image.load('data/sprites/title.png')
    window = pygame.Surface(size)
    screen = pygame.display.set_mode(
        (width*constants.SCREEN_SCALING_FACTOR, height*constants.SCREEN_SCALING_FACTOR))
    game = Game()
    render_masks = False
    while 1:
        # update
        game.process_events()
        game.update_sprites()
        # prepare screen
        window.blit(game.render_map(), (0, 0))
        window.blit(game.render_lights(), (0, 0),
                    special_flags=pygame.BLEND_RGBA_SUB)
        if game.player.title_screen:
            window.blit(title, (77, 50))
        # scale
        scaled_win = pygame.transform.scale(window, screen.get_size())
        screen.blit(scaled_win, (0, 0))
        # update display
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
