import pygame as pg
from ..tools import GameState
from ..constants import GAME_HEIGHT, GAME_WIDTH, BlockType, DEATH_EVENT, Direction, WIN_EVENT, SHOW_MASKS_EVENT, SHOW_TIMER_EVENT, lights, obstacles, SCARE_EVENT, MAP1_TEXT
from .. import sprites
from .. import tilemap
from .. import animations
from ..helpers import render_text
import typing

LIGHT_PATH = "./resources/sprites/spotlight_dark.png"
PLAYER_5 = pg.transform.scale_by(
    pg.image.load(LIGHT_PATH), 2)
LIGHT_FILTER = pg.surface.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)


def load_map(tm: tilemap.GameMap):
    player = None
    coords = []
    for obj in tm.tmxdata.objects:
        if obj.name == 'player_spawn':
            player = sprites.Player(obj.x, obj.y, obj.x, obj.y)
        if obj.name == 'player_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, BlockType.COLLIDE)
        if obj.name == 'death_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, BlockType.DEATH)
            _ = animations.DoomTile()

            if obj.width > 16:
                for i in range(0, int(obj.width), 16):
                    coords.append((obj.x + i, obj.y))

            elif obj.height > 16:
                for i in range(0, int(obj.height), 16):
                    coords.append((obj.x, obj.y+i))
            else:
                coords.append((obj.x, obj.y))
        if obj.name == 'win_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, BlockType.WIN)
        if obj.name == 'scare_collide':
            _ = sprites.Block(obj.x, obj.y, obj.width,
                              obj.height, BlockType.SCARE)
        if obj.name == 'light':
            _ = sprites.Light(obj.x, obj.y, obj.width,
                              obj.height)
    return player, coords


class Map(GameState):
    def __init__(self, map_path, next_state):
        super(Map, self).__init__()
        self.next_state = next_state
        self.map = tilemap.GameMap(map_path, 0, None)
        self.player = None
        self.camera = tilemap.Camera(self.map.width, self.map.height)
        self.show_timer = True
        self.fire_effect = animations.DoomTile()
        self.first_level = False
        if map_path == "./resources/maps/hospital.tmx":
            print("ayo", next_state)
            self.first_level = True
            self.text_box = animations.TextBox(MAP1_TEXT, font_size=8)

    def startup(self, persistent):
        self.persist = persistent
        self.deaths = self.persist['deaths']
        self.timer = self.persist['timer']
        pg.sprite.Group.empty(obstacles)
        pg.sprite.Group.empty(lights)
        self.player, self.fire_coords = load_map(self.map)
        self.fader = animations.Fader()
        self.fader.activate(dir=Direction.IN)
        if self.first_level:
            self.text_box.start()
        self.player.dir = Direction.DOWN

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.quit = True
                return
            if self.first_level and event.key == pg.K_RETURN:
                if self.text_box.paused:
                    self.text_box.paused = False
                    self.text_box.advance_message()
                else:
                    self.text_box.skip_to_end()
        elif event.type == DEATH_EVENT:
            self.persist['deaths'] += 1
            self.player.grid_x = self.player.spawn_x
            self.player.grid_y = self.player.spawn_y
            self.player.dir = Direction.UP
            self.player.anim_step = 0
            self.fader.activate(Direction.IN)
        elif event.type == WIN_EVENT:
            self.done = True
            self.persist['timer'] = self.timer
        elif event.type == SCARE_EVENT:
            self.next_state = "SCARE"
            self.done = True
        elif event.type == SHOW_MASKS_EVENT:
            self.show_masks = not self.show_masks
        elif event.type == SHOW_TIMER_EVENT:
            self.show_timer = not self.show_timer

    def update(self, dt):
        self.timer += dt
        if self.player != None:
            self.player.update()
            self.camera.update(self.player)
            self.fire_effect.update_fire_effect()
            self.fader.update()
            if self.first_level:
                self.text_box.update(dt)

    # def render_fire(self):
    #     temp_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT)).convert_alpha()
    #     for t in fire:
    #         t.rect = self.camera.apply_rect(t.rect)
    #         t.render_fire_effect(temp_surface)
    #     return temp_surface

    def render_map(self):
        temp_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)
        bottom_layer = self.map.draw_layer(None)
        # print(bottom_layer.get_size())
        temp_surface.blit(bottom_layer, self.camera.apply_rect(
            bottom_layer.get_rect()))

        temp_surface.blit(self.player.image, self.camera.apply(self.player))
        # if self.show_masks:
        #    temp_surface = self.render_masks(temp_surface)
        top_layer = self.map.draw_layer('treetop')
        top_layer.set_colorkey((0, 0, 0))
        temp_surface.blit(top_layer,
                          self.camera.apply_rect(top_layer.get_rect()))

        return temp_surface

    def render_fire(self):
        temp_surface = pg.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)
        for (x, y) in self.fire_coords:
            camera_x, camera_y = self.camera.apply_rect(
                pg.Rect(x, y, 0, 0)).topleft
            self.fire_effect.render_fire_effect(
                temp_surface, camera_x, camera_y-16)
        return temp_surface

    def render_lights(self):
        temp_surface = pg.surface.Surface(
            (GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)

        #temp_surface.fill((255, 255, 255, 255))
        # -192 shifts center of light to center of player sprite
        temp_surface.blit(
            # more negative is closer to top left
            PLAYER_5, self.camera.apply_offset(self.player, -(2*192), -(2*192)))
        # for l in pg.sprite.Group.sprites(lights):
        #    temp_surface.blit(
        #        PLAYER_5, self.camera.apply_offset(l, -2*192, -2*192))
        return temp_surface

    def render_hud(self):
        temp_surface = pg.Surface(
            (GAME_WIDTH, GAME_HEIGHT)).convert()
        # Render deaths:
        deaths_label = render_text("DEATHS")
        temp_surface.blit(deaths_label, (0, 25))
        #deaths = render_text(str(self.deaths))
        deaths = render_text(str(self.persist['deaths']))
        temp_surface.blit(deaths, (0, deaths_label.get_height()+25))
        # Render
        level_label = render_text("LVL")
        level = render_text(str(1))
        temp_surface.blit(level_label, (GAME_WIDTH//2 -
                                        (level_label.get_width()//2), 25))
        temp_surface.blit(level, (GAME_HEIGHT//2 -
                                  (level_label.get_width()//2), level_label.get_height() + 25))

        # Render
        timer = render_text(str(self.timer//1000))
        if self.show_timer:
            time_label = render_text("TIME")
            temp_surface.blit(
                time_label, (GAME_WIDTH - time_label.get_width(), 25))
            temp_surface.blit(timer, (GAME_WIDTH -
                                      timer.get_width(), time_label.get_height() + 25))
        temp_surface.set_colorkey((0, 0, 0))
        return temp_surface

    def draw(self, surface):
        INFO = pg.display.Info()
        surf = pg.Surface((GAME_WIDTH, GAME_HEIGHT), pg.SRCALPHA)

        map = self.render_map()
        surf.blit(map, (0, 0))

        fire = self.render_fire()
        surf.blit(fire, (0, 0))

        lights = self.render_lights()
        surf.blit(lights, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        #hud = self.render_hud()
        #surf.blit(hud, (0, 0))

        surf.blit(self.fader.draw(), (0, 0))

        if self.first_level and self.text_box.active:
            surf.blit(self.text_box.draw(), (0, 0))
        else:
            self.player.can_move = True

        sidebar_width = (INFO.current_w - INFO.current_h)//2
        scaled_win = pg.transform.scale(
            surf, (INFO.current_h, INFO.current_h))
        surface.blit(scaled_win, (sidebar_width, 0))
