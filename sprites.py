import pygame
import constants
import helpers

class Player(pygame.sprite.Sprite):
  def __init__(self, color, width, height):
    pygame.sprite.Sprite.__init__(self)

    self.color = color
    self.width = width
    self.height = height

    self.load_sprites("data/booth23sprite_white.png")
    self.rect = self.image.get_rect()

    self.grid_x = 0 
    self.grid_y = 0

  def load_sprites(self, filename):
    ss = helpers.spritesheet(filename, )
    idle = ss.image_at((0, 0, 16, 16), colorkey = -1)
    self.image = idle

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
