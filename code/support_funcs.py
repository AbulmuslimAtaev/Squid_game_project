from PIL import Image
import os
import pygame
import sys


def load_image(path, colorkey=None):
    fullname = os.path.join(path)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(path)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def pic2text(imagename):
    im = Image.open(f'../images/{imagename}.png')
    _WIDTH = 100
    _HEIGHT = 100
    resized_img = im.resize((_WIDTH, _HEIGHT), Image.ANTIALIAS)
    pixels = resized_img.load()
    x, y = resized_img.size
    values = []
    for i in range(x):
        for j in range(y):
            c = pixels[i, j]
            if c[0] <= 100 and c[1] <= 100 and c[2] <= 100:
                values.append((i, j))
    return values


class SpriteMouseLocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)