from typing import Tuple
import pygame
from constants import Direction, GRIDSIZE, obstacles, lights,  DEATH_EVENT, ANIM_SPEED, BlockType, WIN_EVENT, TITLE_SCREEN_TIME, SHOW_MASKS_EVENT
import helpers

# Returns true if any point in points is colliding with any tile


def is_colliding_masks(player, new_x: int, new_y: int, tiles: pygame.sprite.Group) -> BlockType:
    for tile in tiles:
        if player.mask.overlap(tile.mask, (tile.rect.x - new_x, tile.rect.y - new_y)) is not None:
            return tile.type
    return None


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
        self.scare_on_next = False
        self.scare = False

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
        self.mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.grid_x, self.grid_y)
        self.keys()
        self.mask = pygame.mask.from_surface(self.image)

    def test_collision_masks(self, direction: Direction, new_x: int, new_y: int, tiles: pygame.sprite.Group) -> int:
        if direction == Direction.RIGHT:
            new_x += 2
            new_y -= 2
        elif direction == Direction.DOWN:
            new_x -= 2
            new_y += 2
        return is_colliding_masks(self, new_x, new_y, tiles)

    def movement(self, direction: Direction) -> None:
        death_event = pygame.event.Event(DEATH_EVENT)
        win_event = pygame.event.Event(WIN_EVENT)
        if self.anim_step > TITLE_SCREEN_TIME:
            self.title_screen = False
            # self.scare_on_next = True
        match direction:
            case Direction.UP:
                match self.test_collision_masks(Direction.UP, self.grid_x, self.grid_y - self.step_size, obstacles):
                    case None:
                        self.grid_y += -self.step_size
                        self.anim_step += 1
                    case BlockType.DEATH:
                        _ = pygame.event.post(death_event)
                        if self.scare_on_next:
                            self.scare = True
                    case BlockType.WIN:
                        _ = pygame.event.post(win_event)
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
                        _ = pygame.event.post(death_event)
                        if self.scare_on_next:
                            self.scare = True
                    case BlockType.WIN:
                        _ = pygame.event.post(win_event)
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
                        _ = pygame.event.post(death_event)
                        if self.scare_on_next:
                            self.scare = True
                    case BlockType.WIN:
                        _ = pygame.event.post(win_event)
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
                        _ = pygame.event.post(death_event)
                        if self.scare_on_next:
                            self.scare = True
                    case BlockType.WIN:
                        _ = pygame.event.post(win_event)
                    case BlockType.SCARE:
                        self.grid_x += self.step_size
                        self.anim_step = (self.anim_step + 1)
                        self.scare_on_next = True
                self.dir = Direction.RIGHT
        self.image = self.images[self.dir][(self.anim_step//ANIM_SPEED) % 3]

    def keys(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.movement(Direction.UP)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.movement(Direction.LEFT)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.movement(Direction.DOWN)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.movement(Direction.RIGHT)
        elif keys[pygame.K_m]:
            pygame.event.post(pygame.event.Event(SHOW_MASKS_EVENT))


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
        self.mask = pygame.mask.from_surface(pygame.Surface((w, h)))


class Light(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int) -> None:
        pygame.sprite.Sprite.__init__(self, lights)
        self.rect = pygame.Rect(x, y, w, h)
        self.rect.x = x
        self.rect.y = y
