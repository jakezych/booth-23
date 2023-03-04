import pygame 
import sys
from constants import *
import sprites
import tilemap

<<<<<<< Updated upstream
=======
clock = pygame.time.Clock()


obstacles.empty()

map = tilemap.TiledMap("data/level1.tmx")

for tile_object in map.tmxdata.objects:
    if tile_object.name == 'player':
        player = sprites.Player(tile_object.x, tile_object.y,16,16)
    else:
        _ = sprites.Obstacle(tile_object.x, tile_object.y, 16, 16)
>>>>>>> Stashed changes

def main():
  clock = pygame.time.Clock()
  pygame.init()
  size = width, height = constants.WIDTH, constants.HEIGHT
  screen = pygame.display.set_mode(size)
  
  map1 = tilemap.TiledMap("data/level1.tmx")
  
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