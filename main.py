
import pygame
import constants
import game
import media


def main() -> None:
    # Init pygame
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption(constants.WINDOW_CAPTION)
    pygame.mouse.set_visible(False)
    # Play music
    size = constants.WIDTH, constants.HEIGHT
    info = pygame.display.Info()
    screen_w = info.current_w
    screen_h = info.current_h
    window = pygame.Surface(size)
    screen = pygame.display.set_mode(
        (screen_w, screen_h-50))
    # Play music
    pygame.mixer.music.load(media.LEVEL_1_MUSIC)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)
    g = game.Game(screen_w, screen_h)
    while 1:
        # update
        g.process_events()
        g.update_sprites()
        # prepare screen
        scaled_win, loc = g.render_game(window)
        screen.blit(scaled_win, loc)
        # update display
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
