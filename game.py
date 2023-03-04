import pygame 
import pytmx
import sys
import constants

class Player(pygame.sprite.Sprite):
  def __init__(self, color, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.color = color
    self.width = width
    self.height = height

    self.x = 0
    self.y = 0 

    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()
    pygame.draw.rect(self.image, color, [self.x, self.y, width, height])

    self.x_move = 0
    self.y_move = 0


  def update(self):
    self.keys()
    self.move()

  def keys(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.y_move = 1
    if keys[pygame.K_a]:
      self.x_move = -1
    if keys[pygame.K_s]:
      self.y_move = -1
    if keys[pygame.K_d]:
      self.x_move = 1
    
  def move(self):
    self.x += self.x_move
    self.y += self.y_move
    self.rect.x = self.x
    self.rect.y = self.y





clock = pygame.time.Clock()

def main():
  pygame.init()
  # TODO: figure out resolution 
  size = width, height = 320, 240
  black = (0, 0, 0)

  screen = pygame.display.set_mode(size)
  # TODO: consider setting up something like this: https://github.com/Mekire/cabbages-and-kings/tree/master/data
  player = Player(constants.WHITE,50,50)
  
  
  
  while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
          sys.exit()


    player.update()
    screen.blit(player.image, (player.x, player.y))
    screen.fill(black)
    clock.tick(constants.FPS)/1000
    pygame.display.flip()


if __name__ == "__main__":
  main()