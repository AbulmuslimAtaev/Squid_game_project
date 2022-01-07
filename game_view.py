import os
from random import randint
import sys
from itertools import cycle

import pygame
from pillow_part import pic2text

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))
IMAGE_NAME = "cloud"


def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Igla(pygame.sprite.Sprite):
    images = [load_image(f"animation\pic{i}.png", None) for i in range(0, 17)]

    def __init__(self):
        super().__init__(all_sprites)
        self.num = cycle(list(range(0, 17)) + (list(range(16, -1, -1))))
        for i in range(8):
            next(self.num)
        self.image = Igla.images[next(self.num)]
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def turn(self):
        self.image = Igla.images[randint(4, 12)]
        # self.image = Igla.images[next(self.num)]

class Form(pygame.sprite.Sprite):
    image = load_image(f"{IMAGE_NAME}.png", -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Form.image
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Cookie(pygame.sprite.Sprite):
    image = load_image("universla_cookie.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cookie.image
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2


class Spot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("grey"), (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 2
        self.rect.y = pos[1] - 2

    def update(self):
        if not pygame.sprite.collide_mask(self, star_form):
            print("Проиграл")


all_sprites = pygame.sprite.Group()


class Check_Form(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (width - 200) // 2 + pos[0] * 2 - 1
        self.rect.y = (height - 200) // 2 + pos[1] * 2 - 1


def draw_update():
    fg = True
    for i in drawed_check.sprites():
        if not pygame.sprite.spritecollideany(i, drawed):
            fg = False
        else:
            i.kill()
    if not fg:
        return False
    return True

MYEVENTTYPE = pygame.USEREVENT + 1
drawed_check = pygame.sprite.Group()
values = pic2text(IMAGE_NAME)
for i in values:
    drawed_check.add(Check_Form(i))
drawed = pygame.sprite.Group()
check_form = pygame.sprite.Group
running = True
clock = pygame.time.Clock()
cookie = Cookie()
star_form = Form()
igla, flag = Igla(), False
pygame.display.set_caption("PySquid")
pygame.time.set_timer(MYEVENTTYPE, 50)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == MYEVENTTYPE:
            flag = True
    pos = pygame.mouse.get_pos()
    press = pygame.mouse.get_pressed()
    if press[0]:
        if flag:
            igla.turn()
            flag = False
        spot = Spot(pos)
        drawed.add(spot)
        spot.update()
        if draw_update():
            running = False
    all_sprites.update()
    screen.fill(pygame.Color('grey'))
    all_sprites.draw(screen)
    drawed_check.draw(screen)
    if pygame.mouse.get_focused():
        pygame.mouse.set_visible(False)
        igla.move(pos)
    pygame.display.flip()
if not running:
    print("Победа")
pygame.quit()
