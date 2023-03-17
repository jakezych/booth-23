
import pygame
import constants
import game


def main() -> None:
    clock = pygame.time.Clock()
    pygame.init()
    pygame.display.set_caption('PDT Booth23')
    size = width, height = constants.WIDTH, constants.HEIGHT
    title = pygame.image.load('data/sprites/title.png')
    window = pygame.Surface(size)
    info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (info.current_w, info.current_h-50))
    pygame.mixer.music.load('data/music/rbr_splatter.mp3')
    pygame.mixer.music.play(-1)
    g = game.Game()
    while 1:
        # update
        g.process_events()
        g.update_sprites()
        # prepare screen
        window.blit(g.render_map(), (0, 0))
        window.blit(g.render_lights(), (0, 0),
                    special_flags=pygame.BLEND_RGBA_SUB)
        if g.player.title_screen:
            window.blit(title, (77, 50))
        # scale
        #scaled_win = pygame.transform.scale(window, screen.get_size())
        scaled_win = pygame.transform.scale(window, (
            width*constants.SCREEN_SCALING_FACTOR, height*constants.SCREEN_SCALING_FACTOR))
        screen.blit(scaled_win, (340, 0))
        # update display
        clock.tick(constants.FPS)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
