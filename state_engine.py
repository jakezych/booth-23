import sys
import pygame as pg
from src.tools import GameControl
from src.states import gameplay, map, splash, credits, doom_test, scare
from src.constants import FULLSCREEN, WINDOW_CAPTION

if __name__ == "__main__":
    INFO = pg.display.Info()
    if FULLSCREEN:
        screen = pg.display.set_mode(
            (INFO.current_w, INFO.current_h-50), pg.FULLSCREEN)
    else:
        screen = pg.display.set_mode(
            (INFO.current_w, INFO.current_h-50))
    pg.display.set_caption(WINDOW_CAPTION)

    # pg.key.set_repeat(1, 10)
    states = {
        "MAP3": map.Map("./resources/maps/map3.tmx", "CREDITS", 3),
        "HOSPITAL": map.Map("./resources/maps/hospital.tmx", "HIGHWAY", 1),
        "SPLASH": splash.SplashScreen(),
        "CREDITS": credits.CreditScreen(),
        "SCARE": scare.ScareScreen(),
        "HIGHWAY": map.Map("./resources/maps/highway.tmx", "MAP3", 2),
    }
    game = GameControl(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
