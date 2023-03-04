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
      self.check_collision(self.rect, obstacles, Direction.UP)
    elif keys[pygame.K_a]:
      self.grid_x += -constants.GRIDSIZE
      self.check_collision(self.rect, obstacles, Direction.LEFT)
    elif keys[pygame.K_s]:
      self.grid_y += constants.GRIDSIZE
      self.check_collision(self.rect, obstacles, Direction.DOWN)
    elif keys[pygame.K_d]:
      self.grid_x += constants.GRIDSIZE
      self.check_collision(self.rect, obstacles, Direction.RIGHT)

    def check_collision(rect, tiles, direction):
        collisions = collisions_test(rect, tiles)
        for tile in collisions:
            if direction == Direction.up:
                self.grid_y = tile.rect.bottom
            if direction == Direction.right:
                self.grid_x = tile.rect.left
            if direction == Direction.left:
                self.grid_x = tile.rect.right
            if direction == Direction.down:
                self.grid_y = tile.rect.top

    def collision_test(rect,tiles):
        collisions = []
        for tile in tiles:
            if rect.colliderect(tile):
                collisions.append(tile)
        return collisions

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self,obstacles)
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.x = x
        self.rect.y = y