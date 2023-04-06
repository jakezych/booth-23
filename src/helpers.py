import pygame as pg


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)


def render_text(text: str, size=8, color=(255, 0, 0)) -> pg.Surface:
    font = pg.font.Font('./resources/fonts/font.ttf', size)
    # font.set_bold(True)
    # font.set_italic(True)
    rendered = font.render(
        text, False, color)
    return rendered


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pg.image.load(filename).convert()
        except pg.error:
            print('Unable to load spritesheet image:', filename)
            raise SystemExit
    # Load a specific image from a specific rectangle

    def image_at(self, rectangle, colorkey=None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pg.Rect(rectangle)
        image = pg.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, pg.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list

    def images_at(self, rects, colorkey=None):
        "Loads multiple images, supply a list of coordinates"
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images

    def load_strip(self, rect, image_count, colorkey=None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
