import pygame 
import sys

def main():
  pygame.init()
  # TODO: figure out resolution 
  size = width, height = 320, 240
  black = (0, 0, 0)

  screen = pygame.display.set_mode(size)
  # TODO: consider setting up something like this: https://github.com/Mekire/cabbages-and-kings/tree/master/data
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()

    screen.fill(black)
    pygame.display.flip()

if __name__ == "__main__":
  main()