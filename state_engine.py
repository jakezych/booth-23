import sys
import pygame as pg
from src.tools import GameControl
from src.states import gameplay, map, splash, credits, doom_test, scare
from src.constants import FULLSCREEN

if __name__ == "__main__":
    INFO = pg.display.Info()
    if FULLSCREEN:
        screen = pg.display.set_mode(
            (INFO.current_w, INFO.current_h-50), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(
            (INFO.current_w, INFO.current_h-50))
    from src.constants import WINDOW_CAPTION
    pg.display.set_caption(WINDOW_CAPTION)
    states = {"MAP1": map.Map("./resources/maps/map1.tmx", "MAP2"),
              "MAP2": map.Map("./resources/maps/map2.tmx", "MAP3"),
              "MAP3": map.Map("./resources/maps/map3.tmx", "CREDITS"),
              "HOSPITAL": map.Map("./resources/maps/hospital.tmx", "MAP2"),
              "SPLASH": splash.SplashScreen(),
              "CREDITS": credits.CreditScreen(),
              # "DOOM": doom_test.DoomTest(),
              "SCARE": scare.ScareScreen(),
              }
    game = GameControl(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
