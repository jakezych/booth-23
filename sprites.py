import pygame
import constants

class Player(pygame.sprite.Sprite):
  def __init__(self, color, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.color = color
    self.width = width
    self.height = height

    self.image = pygame.Surface([width, height])
    self.image.fill(color)
    self.rect = self.image.get_rect()

    self.grid_x = 0 
    self.grid_y = 0

    pygame.draw.rect(self.image, color, [self.grid_x, self.grid_y, width, height])


  def update(self):
    self.keys()

  def keys(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.grid_y += -constants.GRIDSIZE
    elif keys[pygame.K_a]:
      self.grid_x += -constants.GRIDSIZE
    elif keys[pygame.K_s]:
      self.grid_y += constants.GRIDSIZE
    elif keys[pygame.K_d]:
      self.grid_x += constants.GRIDSIZE
