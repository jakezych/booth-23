import pygame 
import sys
import constants
import sprites
import tilemap

clock = pygame.time.Clock()


map = tilemap.TiledMap("data/levels/level1.tmx")

for tile_object in map.tmxdata.objects:
    if tile_object.name == 'player':
            player = sprites.Player(tile_object.x, tile_object.y,16,16)

def main():
  pygame.init()
  size = width, height = constants.WIDTH, constants.HEIGHT
  screen = pygame.display.set_mode(size)
  # TODO: consider setting up something like this: https://github.com/Mekire/cabbages-and-kings/tree/master/data
  player = sprites.Player(constants.WHITE,32,32)
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()

    player.update()

    map_img = map.make_map()
    map_rect = map_img.get_rect()

    screen.blit(map_img, 0,0)
    screen.blit(player.image,(player.grid_x, player.grid_y))
    clock.tick(constants.FPS)
    pygame.display.flip()


if __name__ == "__main__":
  main()