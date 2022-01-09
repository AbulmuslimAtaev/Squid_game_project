import os
from random import randint
import sys
from itertools import cycle

import pygame
from pillow_part import pic2text
from pygame.sprite import *
from UT import *
from test_menu import main

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))


class Sprite_Mouse_Location(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


def go_to_pause():
    menu = UMenu(screen)
    back_btn = UBackButton(menu, (600, 400, 100, 100), main)
    ps_menu = UPauseMenu(menu)
    ps_menu.addButton('Resume', menu.close)
    ps_menu.addButton('Quit', pygame.quit)
    menu.mainloop(False)


class PauseButton(pygame.sprite.Sprite):
    def __init__(self):
        super(PauseButton, self).__init__(all_sprites)
        self.image = pygame.transform.scale(load_image('pause.png'), (50, 50))
        self.rect = self.image.get_rect()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            go_to_pause()
            return True


def load_image(name, colorkey=None):
    fullname = os.path.join('../../Desktop/banjo/PROJECT2_SQUID_DALGONA_CANDY/images', name)
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
    def __init__(self, image_name):
        super().__init__(all_sprites)
        self.image = load_image(f"{image_name}.png", -1)
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
        super().__init__()
        self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("grey"), (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 2
        self.rect.y = pos[1] - 2
        if not pygame.sprite.collide_mask(self, star_form):
            print("Проиграл")


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


def game_run(image_name, menu):
    def close_menu():
        menu.close()
    global gen_menu
    gen_menu = menu
    MYEVENTTYPE = pygame.USEREVENT + 1
    global all_sprites
    all_sprites = pygame.sprite.Group()
    global drawed_check
    drawed_check = pygame.sprite.Group()
    values = pic2text(image_name)
    for i in values:
        drawed_check.add(Check_Form(i))
        global drawed
    drawed = pygame.sprite.Group()
    global check_form
    check_form = pygame.sprite.Group
    running = True
    clock = pygame.time.Clock()
    global cookie
    cookie = Cookie()
    global star_form
    star_form = Form(image_name)
    pause = PauseButton()
    igla, flag = Igla(), False
    pygame.display.set_caption("PySquid")
    pygame.time.set_timer(MYEVENTTYPE, 50)
    mouse_sprite = Sprite_Mouse_Location()
    pause_flag = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MYEVENTTYPE:
                flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                pause_flag = pause.click_check(mouse_sprite)

        pos = pygame.mouse.get_pos()
        press = pygame.mouse.get_pressed()

        if press[0]:
            if not pause_flag:
                if flag:
                    igla.turn()
                    flag = False
                spot = Spot(pos)
                drawed.add(spot)
                if draw_update():
                    running = False

        screen.fill(pygame.Color('grey'))
        all_sprites.draw(screen)
        drawed.draw(screen)

        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            igla.move(pos)
        pygame.display.flip()
    if not running:
        print("Победа")
    close_menu()


if __name__ == '__main__':
    game_run('star4')
