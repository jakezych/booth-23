import pygame
from constants import Direction, GRIDSIZE, obstacles
import helpers

# Returns true if any point in points is colliding with any tile
def is_colliding(points : list[(int,int)], tiles : pygame.sprite.Group):
    for tile in tiles:
        for point in points:
            if tile.rect.collidepoint(point):
                return True
    return False

class Player(pygame.sprite.Sprite):
    def __init__(self, color, width, height, start_x, start_y):
        pygame.sprite.Sprite.__init__(self)
        # Set basic properties
        self.color = color
        self.width = width
        self.height = height
        self.step_size = GRIDSIZE//4
        # Set starting conditions
        self.grid_x = start_x
        self.grid_y = start_y
        self.anim_step = 0
        self.dir = Direction.DOWN
        # Intialize sprite and rect
        self.load_sprites()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)

    def load_sprites(self, filename : str= "data/sprites/booth23sprite_white.png"):
        ss = helpers.spritesheet(filename, )
        idle = ss.image_at((0, 0, 16, 16), colorkey = -1)
        self.images = {}
        self.images[Direction.DOWN] = ss.images_at([(0, 0, 16, 16),(16,0,16,16), (32, 0,16,16)], colorkey = -1)
        self.images[Direction.UP] = ss.images_at([(112,0,16,16), (96,0,16,16), (0,16,16,16)], colorkey=-1)
        self.images[Direction.RIGHT] = ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)
        self.images[Direction.LEFT] = ss.images_at([(48, 16,16,16), (64,16,16,16), (80,16,16,16)], colorkey=-1)
        #self.images[Direction.LEFT] = [pygame.transform.flip(x, flip_x=True, flip_y=False) for x in ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)]
        self.image = self.images[Direction.DOWN][self.anim_step]

    def update(self):
        self.keys()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)

    def test_collision(self, direction: Direction, new_x :int, new_y:int, tiles : pygame.sprite.Group):
        if direction == direction.UP:
            p1, p2, p3 = (new_x, new_y), (new_x+GRIDSIZE, new_y), (new_x+GRIDSIZE/2, new_y)
        elif direction == direction.DOWN:
            p1, p2, p3 =(new_x, new_y+GRIDSIZE), (new_x+GRIDSIZE, new_y+GRIDSIZE), (new_x+GRIDSIZE/2, new_y+GRIDSIZE)
        elif direction == direction.LEFT:
            p1, p2, p3 = (new_x, new_y), (new_x, new_y+GRIDSIZE), (new_x, new_y+GRIDSIZE/2)
        elif direction == direction.RIGHT:
            p1, p2, p3 = (new_x+GRIDSIZE, new_y), (new_x+GRIDSIZE, new_y+GRIDSIZE), (new_x+GRIDSIZE/2, new_y+GRIDSIZE)
        collision = is_colliding([p1, p2, p3], tiles)
        return collision

    def keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.dir = Direction.UP
            if not self.test_collision(Direction.UP, self.grid_x, self.grid_y - self.step_size, obstacles):
                self.grid_y += -self.step_size
                self.anim_step = (self.anim_step + 1) % 3
        elif keys[pygame.K_a]:
            self.dir = Direction.LEFT
            if not self.test_collision(Direction.LEFT, self.grid_x-self.step_size, self.grid_y, obstacles):
                self.grid_x += -self.step_size
                self.anim_step = (self.anim_step + 1) % 3
        elif keys[pygame.K_s]:
            self.dir = Direction.DOWN
            if not self.test_collision(Direction.DOWN, self.grid_x, self.grid_y + self.step_size, obstacles):
                self.grid_y += self.step_size
                self.anim_step = (self.anim_step + 1) % 3
        elif keys[pygame.K_d]:
            self.dir = Direction.RIGHT
            if not self.test_collision(Direction.RIGHT, self.grid_x+self.step_size, self.grid_y, obstacles):
                self.grid_x += self.step_size
                self.anim_step = (self.anim_step + 1) % 3
        self.image = self.images[self.dir][self.anim_step]
class Demogorgon(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        ss = helpers.spritesheet("data/sprites/demagorgon.png", )
        stand = ss.image_at((0, 0, 32, 64), colorkey = -1)
        self.x = x
        self.y = y
        self.image = stand
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,x,y,w,h):
        pygame.sprite.Sprite.__init__(self, obstacles)
        self.rect = pygame.Rect(x,y,w,h)
        self.rect.x = x
        self.rect.y = y

