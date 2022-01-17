from random import randint
from PIL import Image
import os
import pygame
import sys


def load_image(path, colorkey=None, flag=True):
    if flag:
        fullname = os.path.join(path)
        if not os.path.isfile(fullname):
            print(f"Файл с изображением '{path}' не найден")
            sys.exit(0)
        image = pygame.image.load(fullname)
    else:
        image = pygame.image.fromstring(path.tobytes(), path.size, path.mode)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def pic2text(imagename):
    c = (196, 115, 43), (243, 179, 102)
    im = Image.open(f'../images/{imagename}.png')
    _WIDTH = 100
    _HEIGHT = 100
    resized_img1 = im.resize((_WIDTH, _HEIGHT), Image.ANTIALIAS)
    resized_img = resized_img1.copy()
    pixels = resized_img.load()
    x, y = resized_img.size
    values = []
    for i in range(x):
        for j in range(y):
            pix = pixels[i, j]
            if pix[0] <= 100 and pix[1] <= 100 and pix[2] <= 100:
                values.append((i, j))
                r = randint(0, 100)
                if r >= 2:
                    pixels[i, j] = (randint(c[0][0], c[1][0]), randint(c[0][1], c[1][1]), (randint(c[0][2], c[1][2])))
                else:
                    pixels[i, j] = (255, 255, 255, 0)
            else:
                pixels[i, j] = (255, 255, 255, 0)
    return values, resized_img


class SpriteMouseLocation(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


def draw_update(in_group, group_to_check):
    count = 0
    fg = True
    for i in in_group.sprites():
        if not pygame.sprite.spritecollideany(i, group_to_check):
            fg = False
            count += 1
        else:
            i.kill()
    if not fg:
        return False, count
    return True, 0
