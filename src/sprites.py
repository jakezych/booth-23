from typing import Tuple
import pygame as pg
from .constants import BlockType, GRIDSIZE, Direction, DEATH_EVENT, WIN_EVENT, SHOW_TIMER_EVENT, SHOW_MASKS_EVENT, obstacles, lights, ANIM_SPEED, SCARE_EVENT
from . import helpers


def is_colliding_masks(player, new_x: int, new_y: int, tiles: pg.sprite.Group):
    for tile in tiles:
        if player.mask.overlap(tile.mask, (tile.rect.x - new_x, tile.rect.y - new_y)) is not None:
            return tile.type
    return None


class Player(pg.sprite.Sprite):
    def __init__(self, width: int, height: int, start_x: int, start_y: int) -> None:
        pg.sprite.Sprite.__init__(self)
        # Set basic properties
        self.width = width
        self.height = height
        self.spawn_x = start_x
        self.spawn_y = start_y
        self.step_size = GRIDSIZE//8
        # Set starting conditions
        self.grid_x = start_x
        self.grid_y = start_y
        self.anim_step = 0
        self.dir = Direction.DOWN
        # Intialize sprite and rect
        self.load_sprites()
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)
        self.show_title_screen = True
        self.scare_on_next = False

    def load_sprites(self, filename: str = "./resources/sprites/booth23sprite_white.png"):
        ss = helpers.spritesheet(filename, )
        self.images = {}
        self.images[Direction.DOWN] = ss.images_at(
            [(0, 32, 16, 16), (16, 32, 16, 16), (32, 32, 16, 16)], colorkey=-1)
        self.images[Direction.UP] = ss.images_at(
            [(112, 32, 16, 16), (96, 32, 16, 16), (0, 48, 16, 16)], colorkey=-1)
        self.images[Direction.RIGHT] = ss.images_at(
            [(48, 32, 16, 16), (64, 32, 16, 16), (80, 32, 16, 16)], colorkey=-1)
        self.images[Direction.LEFT] = ss.images_at(
            [(48, 48, 16, 16), (64, 48, 16, 16), (80, 48, 16, 16)], colorkey=-1)
        #self.images[Direction.LEFT] = [pygame.transform.flip(x, flip_x=True, flip_y=False) for x in ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)]
        self.image = self.images[Direction.DOWN][self.anim_step]
        self.mask = pg.mask.from_surface(self.image)

    def update(self) -> None:
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)
        self.keys()
        self.mask = pg.mask.from_surface(self.image)

    def test_collision_masks(self, direction: Direction, new_x: int, new_y: int, tiles: pg.sprite.Group) -> int:
        if direction == Direction.RIGHT:
            new_x += 2
            new_y -= 2
        elif direction == Direction.DOWN:
            new_x -= 2
            new_y += 2
        return is_colliding_masks(self, new_x, new_y, tiles)

    def movement(self, direction: Direction) -> None:
        death_event = pg.event.Event(DEATH_EVENT)
        win_event = pg.event.Event(WIN_EVENT)
        scare_event = pg.event.Event(SCARE_EVENT)
        match direction:
            case Direction.UP:
                match self.test_collision_masks(Direction.UP, self.grid_x, self.grid_y - self.step_size, obstacles):
                    case None:
                        self.grid_y += -self.step_size
                        self.anim_step += 1
                    case BlockType.DEATH:
                        if self.scare_on_next:
                            _ = pg.event.post(scare_event)
                        else:
                            _ = pg.event.post(death_event)
                    case BlockType.WIN:
                        _ = pg.event.post(win_event)
                    case BlockType.SCARE:
                        self.grid_y += -self.step_size
                        self.anim_step += 1
                        self.scare_on_next = True
                self.dir = Direction.UP
            case Direction.LEFT:
                match self.test_collision_masks(Direction.LEFT, self.grid_x-self.step_size, self.grid_y, obstacles):
                    case None:
                        self.grid_x += -self.step_size
                        self.anim_step += 1
                    case BlockType.DEATH:
                        if self.scare_on_next:
                            _ = pg.event.post(scare_event)
                        else:
                            _ = pg.event.post(death_event)
                    case BlockType.WIN:
                        _ = pg.event.post(win_event)
                    case BlockType.SCARE:
                        self.grid_x += -self.step_size
                        self.anim_step += 1
                        self.scare_on_next = True
                self.dir = Direction.LEFT
            case Direction.DOWN:
                match self.test_collision_masks(Direction.DOWN, self.grid_x+self.step_size, self.grid_y, obstacles):
                    case None:
                        self.grid_y += self.step_size
                        self.anim_step += 1
                    case BlockType.DEATH:
                        if self.scare_on_next:
                            _ = pg.event.post(scare_event)
                        else:
                            _ = pg.event.post(death_event)
                    case BlockType.WIN:
                        _ = pg.event.post(win_event)
                    case BlockType.SCARE:
                        self.grid_y += self.step_size
                        self.anim_step += 1
                        self.scare_on_next = True
                self.dir = Direction.DOWN
            case Direction.RIGHT:
                match self.test_collision_masks(Direction.RIGHT, self.grid_x, self.grid_y+self.step_size, obstacles):
                    case None:
                        self.grid_x += self.step_size
                        self.anim_step = (self.anim_step + 1)
                    case BlockType.DEATH:
                        if self.scare_on_next:
                            _ = pg.event.post(scare_event)
                        else:
                            _ = pg.event.post(death_event)
                    case BlockType.WIN:
                        _ = pg.event.post(win_event)
                    case BlockType.SCARE:
                        self.grid_x += self.step_size
                        self.anim_step = (self.anim_step + 1)
                        self.scare_on_next = True
                self.dir = Direction.RIGHT
        self.image = self.images[self.dir][(self.anim_step//ANIM_SPEED) % 3]

    def keys(self) -> None:
        keys = pg.key.get_pressed()
        if keys[pg.K_w] or keys[pg.K_UP]:
            self.movement(Direction.UP)
        elif keys[pg.K_a] or keys[pg.K_LEFT]:
            self.movement(Direction.LEFT)
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            self.movement(Direction.DOWN)
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            self.movement(Direction.RIGHT)
        elif keys[pg.K_m]:
            pg.event.post(pg.event.Event(SHOW_MASKS_EVENT))
        elif keys[pg.K_t]:
            pg.event.post(pg.event.Event(SHOW_TIMER_EVENT))


class Block(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, type: BlockType) -> None:
        pg.sprite.Sprite.__init__(self, obstacles)
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.type = type
        self.mask = pg.mask.from_surface(pg.Surface((w, h)))


class Light(pg.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        pg.sprite.Sprite.__init__(self, lights)
        self.rect = pg.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
