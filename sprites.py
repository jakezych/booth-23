from typing import Tuple
import pygame
from constants import Direction, GRIDSIZE, obstacles, lights,  DEATH_EVENT, ANIM_SPEED, BlockType, WIN_EVENT, TITLE_SCREEN_TIME
import helpers

# Returns true if any point in points is colliding with any tile


def is_colliding(points: list[(int, int)], tiles: pygame.sprite.Group) -> int:
    for tile in tiles:
        for point in points:
            if point is not None and tile.rect.collidepoint(point):
                if tile.type == BlockType.DEATH:
                    return 2
                elif tile.type == BlockType.WIN:
                    return 3
                return 1
    return 0


class Player(pygame.sprite.Sprite):
    def __init__(self, color: Tuple[int, int, int], width: int, height: int, start_x: int, start_y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        # Set basic properties
        self.color = color
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
        self.title_screen = True

    def load_sprites(self, filename: str = "data/sprites/booth23sprite_white.png") -> None:
        ss = helpers.spritesheet(filename, )
        self.images = {}
        self.images[Direction.DOWN] = ss.images_at(
            [(0, 0, 16, 16), (16, 0, 16, 16), (32, 0, 16, 16)], colorkey=-1)
        self.images[Direction.UP] = ss.images_at(
            [(112, 0, 16, 16), (96, 0, 16, 16), (0, 16, 16, 16)], colorkey=-1)
        self.images[Direction.RIGHT] = ss.images_at(
            [(48, 0, 16, 16), (64, 0, 16, 16), (80, 0, 16, 16)], colorkey=-1)
        self.images[Direction.LEFT] = ss.images_at(
            [(48, 16, 16, 16), (64, 16, 16, 16), (80, 16, 16, 16)], colorkey=-1)
        #self.images[Direction.LEFT] = [pygame.transform.flip(x, flip_x=True, flip_y=False) for x in ss.images_at([(48, 0,16,16), (64,0,16,16), (80,0,16,16)], colorkey=-1)]
        self.image = self.images[Direction.DOWN][self.anim_step]

    def update(self) -> None:
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)
        self.keys()

    def test_collision(self, direction: Direction, new_x: int, new_y: int, tiles: pygame.sprite.Group) -> int:
        if direction == direction.UP:
            p1, p2 = (new_x, new_y), (new_x+GRIDSIZE/2, new_y)
        elif direction == direction.DOWN:
            p1, p2 = (new_x, new_y+GRIDSIZE), (new_x +
                                               GRIDSIZE/2, new_y+GRIDSIZE)
        elif direction == direction.LEFT:
            p1, p2 = (new_x, new_y), (new_x, new_y+GRIDSIZE/2)
        elif direction == direction.RIGHT:
            p1, p2 = (new_x+GRIDSIZE, new_y), (new_x+GRIDSIZE/2, new_y)
        collision = is_colliding([p1, p2], tiles)
        return collision

    def movement(self, direction: Direction) -> None:
        death_event = pygame.event.Event(DEATH_EVENT)
        win_event = pygame.event.Event(WIN_EVENT)
        if self.anim_step > TITLE_SCREEN_TIME:
            self.title_screen = False
        match direction:
            case Direction.UP:
                match self.test_collision(Direction.UP, self.grid_x, self.grid_y - self.step_size, obstacles):
                    case 3:
                        _ = pygame.event.post(win_event)
                    case 2:
                        s = pygame.event.post(death_event)
                    case 1:
                        pass
                    case 0:
                        self.grid_y += -self.step_size
                        self.anim_step += 1
                self.dir = Direction.UP
            case Direction.LEFT:
                match self.test_collision(Direction.LEFT, self.grid_x-self.step_size, self.grid_y, obstacles):
                    case 3:
                        _ = pygame.event.post(win_event)
                    case 2:
                        s = pygame.event.post(death_event)
                    case 1:
                        pass
                    case 0:
                        self.grid_x += -self.step_size
                        self.anim_step += 1
                self.dir = Direction.LEFT
            case Direction.DOWN:
                match self.test_collision(Direction.DOWN, self.grid_x, self.grid_y, obstacles):
                    case 3:
                        _ = pygame.event.post(win_event)
                    case 2:
                        s = pygame.event.post(death_event)
                    case 1:
                        pass
                    case 0:
                        self.grid_y += self.step_size
                        self.anim_step += 1
                self.dir = Direction.DOWN
            case Direction.RIGHT:
                match self.test_collision(Direction.RIGHT, self.grid_x, self.grid_y, obstacles):
                    case 3:
                        _ = pygame.event.post(win_event)
                    case 2:
                        s = pygame.event.post(death_event)
                    case 1:
                        pass
                    case 0:
                        self.grid_x += self.step_size
                        self.anim_step = (self.anim_step + 1)
                self.dir = Direction.RIGHT
        self.image = self.images[self.dir][(self.anim_step//ANIM_SPEED) % 3]

    def keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.movement(Direction.UP)
        elif keys[pygame.K_a]:
            self.movement(Direction.LEFT)
        elif keys[pygame.K_s]:
            self.movement(Direction.DOWN)
        elif keys[pygame.K_d]:
            self.movement(Direction.RIGHT)


class Demogorgon(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int) -> None:
        pygame.sprite.Sprite.__init__(self)
        ss = helpers.spritesheet("data/sprites/demagorgon.png", )
        stand = ss.image_at((0, 0, 32, 64), colorkey=-1)
        self.x = x
        self.y = y
        self.image = stand
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)

    def update(self) -> None:
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)


class Block(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, type: BlockType) -> None:
        pygame.sprite.Sprite.__init__(self, obstacles)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
        self.type = type


class Light(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        pygame.sprite.Sprite.__init__(self, lights)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
