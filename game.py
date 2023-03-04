import pygame 
import sys
import constants
import sprites

clock = pygame.time.Clock()

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
    screen.fill(constants.BLACK)
    screen.blit(player.image,(player.grid_x, player.grid_y))
    clock.tick(constants.FPS)
    pygame.display.flip()


if __name__ == "__main__":
  main()