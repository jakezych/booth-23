import pygame 
import sys
import constants
import sprites
import tilemap


def main():
  clock = pygame.time.Clock()
  pygame.init()
  size = width, height = constants.WIDTH, constants.HEIGHT
  screen = pygame.display.set_mode(size)
  
  map1 = tilemap.TiledMap("data/level1.tmx")
  
  for tile_object in map1.tmxdata.objects:
    _ = sprites.Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
  # TODO: consider setting up something like this: https://github.com/Mekire/cabbages-and-kings/tree/master/data
  player = sprites.Player(constants.WHITE,16,16)
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()
    player.update()

    map_img = map1.make_map()
    map_rect = map_img.get_rect()
    screen.blit(map_img, (0,0))
    screen.blit(player.image,(player.grid_x, player.grid_y))
    clock.tick(constants.FPS)
    pygame.display.flip()


if __name__ == "__main__":
  main()