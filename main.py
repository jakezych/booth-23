import pygame 
import sys
import os
import constants
import sprites
import tilemap

def load_map(map: tilemap.TiledMap):  
  player = None
  for obj in map.tmxdata.objects:
    if obj.name == 'player_spawn':
      print(obj.x, obj.y)
      player = sprites.Player(None, 0,0, obj.x, obj.y)
    if obj.name == 'player_collide':
      ob = sprites.Obstacle(obj.x, obj.y, obj.width, obj.height)
  return player

def main():

  clock = pygame.time.Clock()
  pygame.init()
  pygame.display.set_caption('PDT Booth23')
  size = width, height = constants.WIDTH, constants.HEIGHT
  
  light=pygame.image.load('data/spotlights/spotlight1.png')
  filter = pygame.surface.Surface(size)

  win = pygame.Surface(size)
  screen = pygame.display.set_mode((width*constants.SCREEN_SCALING_FACTOR, height*constants.SCREEN_SCALING_FACTOR))

  title_map = tilemap.TiledMap("data/maps/title_map/title_map.tmx")

  player = load_map(title_map)
  # dg = sprites.Demogorgon(288,96)
  camera = tilemap.Camera(title_map.width, title_map.height)

  active_map = title_map

  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()
    
    player.update()
    camera.update(player)

    map_img_bot = active_map.make_map()
    map_img_top = active_map.make_map_top()
    map_img_top.set_colorkey((0,0,0))
    map_rect = map_img_bot.get_rect()

    # Blit lighting filter (should actually be after??)
    filter.fill(pygame.color.Color('whitesmoke'))
    # -42 shifts center of light to center of player sprite
    filter.blit(light, camera.apply_offset(player, -42,-42))

    # Blit game elements onto the window
    win.blit(map_img_bot, camera.apply_rect(map_rect))
    # win.blit(dg.image, camera.apply(dg))
    win.blit(player.image,camera.apply(player))
    win.blit(map_img_top, camera.apply_rect(map_rect))
    win.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    # Scale the window to the screen size 
    scaled_win = pygame.transform.scale(win, screen.get_size())
    screen.blit(scaled_win, (0, 0))
   
    clock.tick(constants.FPS)
    pygame.display.flip()


if __name__ == "__main__":
  main()