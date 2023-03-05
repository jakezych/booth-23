import pygame 
import sys
import constants
import sprites
import tilemap

def main():
  clock = pygame.time.Clock()
  pygame.init()
  pygame.display.set_caption('PDT Booth23')
  size = width, height = constants.WIDTH, constants.HEIGHT
  
  light=pygame.image.load('data/circle2.png')
  filter = pygame.surface.Surface(size)
  win = pygame.Surface(size)
  screen = pygame.display.set_mode((width*3, height*3))

  map1 = tilemap.TiledMap("data/forest.tmx")
  for tile_object in map1.tmxdata.objects:
    _ = sprites.Obstacle(tile_object.x, tile_object.y, tile_object.width, tile_object.height)
  
  player = sprites.Player(constants.WHITE,16,16)
  camera = tilemap.Camera(constants.WIDTH*2, constants.HEIGHT*2)

  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()
    
    player.update()
    camera.update(player)

    map_img = map1.make_map()
    map_rect = map_img.get_rect()

    filter.fill(pygame.color.Color('WHITE'))
    filter.blit(light, camera.apply_offset(player, -40,-40))

    win.blit(map_img, camera.apply_rect(map_rect))
    win.blit(player.image,camera.apply(player))
    win.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    scaled_win = pygame.transform.scale(win, screen.get_size())
    screen.blit(scaled_win, (0, 0))
   
    clock.tick(constants.FPS)
    pygame.display.flip()


if __name__ == "__main__":
  main()