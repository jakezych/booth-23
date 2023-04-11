import pygame as pg
from . import helpers
import random
from .constants import Direction, car_spawners, cars, WHITE, GAME_WIDTH

CAR_SHEET_PATH = "./resources/sprites/cars_mid.png"
CAR_SPAWN_MAX_FREQ = 100

SS = helpers.spritesheet(CAR_SHEET_PATH, )
CAR_SPRITES = []
for w in range(0, 300, 60):
    for h in range(0, 80, 40):
        CAR_SPRITES.append((w, h, 60, 40))
# TRUCKS = []
# for w in range(0, 64, 64):
#    for h in range(384, 512, 32):
#        TRUCKS.append((w, h, 64, 32))
CAR_SPRITES = SS.images_at(CAR_SPRITES, colorkey=WHITE)
# TRUCKS = SS.images_at(TRUCKS, colorkey=WHITE)
TOGETHER = CAR_SPRITES  # + TRUCKS


class Car(pg.sprite.Sprite):
    def __init__(self, spawn_x, spawn_y, dir):
        pg.sprite.Sprite.__init__(self, cars)
        self.spawn_x, self.spawn_y = spawn_x, spawn_y
        self.image = random.choice(TOGETHER)
        self.dir = dir
        if self.dir == Direction.LEFT:
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.spawn_x, self.spawn_y)
        self.mask = pg.mask.from_surface(self.image)
        self.x = spawn_x
        self.y = spawn_y
        self.speed = random.uniform(4.5, 4.75)

    def update(self):
        if self.dir == Direction.LEFT:
            self.x -= self.speed
        else:
            self.x += self.speed
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.mask = pg.mask.from_surface(self.image)
        if self.x < -self.rect.width:
            self.kill()
        if self.x > 640:
            self.kill()


class CarSpawner(pg.sprite.Sprite):
    def __init__(self, x, y, dir, w=16, h=16):
        pg.sprite.Sprite.__init__(self, car_spawners)
        self.x = x
        self. y = y
        self.w = w
        self. h = h
        self.dir = dir
        self.random_time = 0
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > self.random_time:
            _ = Car(self.x, self.y, self.dir)
            self.random_time = random.randint(
                CAR_SPAWN_MAX_FREQ//2, CAR_SPAWN_MAX_FREQ)
            self.timer = 0
