import pygame
from constants import Direction, GRIDSIZE, obstacles
import helpers

def collision_test(self, rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        pygame.sprite.Sprite.__init__(self)

        self.color = color
        self.width = width
        self.height = height
        self.step_size = GRIDSIZE//4

        self.grid_x = 0 
        self.grid_y = 0
        self.anim_step = 0
        self.dir = Direction.DOWN
        self.load_sprites()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)

    def load_sprites(self, filename = "data/booth23sprite_white.png"):
        ss = helpers.spritesheet(filename, )
        idle = ss.image_at((0, 0, 16, 16), colorkey = -1)
        self.images = {}
        self.images[Direction.DOWN] = ss.images_at([(0, 0, 16, 16),(16,0,16,16), (32, 0,16,16)], colorkey = -1)
        self.images[Direction.UP] = ss.images_at([(112,0,16,16), (96,0,16,16), (0,16,16,16)], colorkey=-1)
        self.images[Direction.RIGHT] = ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)
        self.images[Direction.LEFT] = [pygame.transform.flip(x, flip_x=True, flip_y=False) for x in ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)]
        self.image = self.images[Direction.DOWN][self.anim_step]
        
    def check_collision(self, rect, tiles, direction):
        collisions = self.collision_test(rect, tiles)
        for tile in collisions:
            if direction == Direction.up:
                self.grid_y = tile.rect.bottom
            if direction == Direction.right:
                self.grid_x = tile.rect.left
            if direction == Direction.left:
                self.grid_x = tile.rect.right
            if direction == Direction.down:
                self.grid_y = tile.rect.top

    def update(self):
        self.keys()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)

    def keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.grid_y += -self.step_size
            self.dir = Direction.UP
            self.anim_step = (self.anim_step + 1) % 3
            #self.check_collision(self.rect, obstacles, Direction.UP)
        elif keys[pygame.K_a]:
            self.grid_x += -self.step_size
            self.dir = Direction.LEFT
            self.anim_step = (self.anim_step + 1) % 3
            #self.check_collision(self.rect, obstacles, Direction.LEFT)
        elif keys[pygame.K_s]:
            self.grid_y += self.step_size
            self.dir = Direction.DOWN
            self.anim_step = (self.anim_step + 1) % 3
            #self.check_collision(self.rect, obstacles, Direction.DOWN)
        elif keys[pygame.K_d]:
            self.grid_x += self.step_size
            self.dir = Direction.RIGHT
            self.anim_step = (self.anim_step + 1) % 3
        self.image = self.images[self.dir][self.anim_step]
            #self.check_collision(self.rect, obstacles, Direction.RIGHT)
        
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self, obstacles)
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.x = x
        self.rect.y = y

