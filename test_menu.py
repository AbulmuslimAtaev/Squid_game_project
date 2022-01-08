import os
import sys
import pygame
from pygame.sprite import *


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


class UWidget(pygame.sprite.Sprite):
    def __init__(self, menu):
        super(UWidget, self).__init__()
        self.menu = menu
        self.count = self.menu.addWidget(self)

    def pos_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.hover(True)
            return True
        else:
            self.hover(False)
            return False

    def hover(self, flag):
        pass

    def draw(self):
        pass


class UButton(UWidget):
    def __init__(self, menu, func, text='', img='', pos=(), flag=True):
        super(UButton, self).__init__(menu)
        self.text = text
        self.pos = pos
        self.flag = flag
        if self.pos != ():
            self.flag = False
        if img != '':
            self.text = False
        else:
            self.img = img
        self.func = func

    def draw(self, color='black'):
        if self.text:
            font = pygame.font.Font(pygame.font.match_font('digiface'), 50)
            text_pg = font.render(self.text, True, (255, 255, 255))
        else:
            text_pg = load_image('music.png', -1)
        if not self.flag:
            print(self.pos)
            text_x = self.pos[2] - text_pg.get_height() // 2
            text_y = self.pos[3] - text_pg.get_height() // 2 + 50 * self.count
            self.image = pygame.Surface((text_pg.get_width() + 20, text_pg.get_height() + 10), pygame.SRCALPHA)

            self.rect = self.image.get_rect()
            self.rect.x = text_x
            self.rect.y = text_y
            pygame.draw.rect(self.image, pygame.Color(color), (self.pos[0],
                                                               self.pos[1],
                                                               self.pos[2],
                                                               self.pos[3]), border_radius=20)
            self.image.blit(text_pg, (10, 0))
        else:
            text_x = self.menu.rect.w // 2 - text_pg.get_width() // 2
            text_y = self.menu.rect.h // 2 - text_pg.get_height() // 2 + 50 * self.count
            self.image = pygame.Surface((text_pg.get_width() + 20, text_pg.get_height() + 10), pygame.SRCALPHA)

            self.rect = self.image.get_rect()
            self.rect.x = text_x
            self.rect.y = text_y
            pygame.draw.rect(self.image, pygame.Color(color), (0, 0,
                                                               text_pg.get_width() + 20,
                                                               text_pg.get_height() + 10), border_radius=20)
            self.image.blit(text_pg, (10, 0))

    def hover(self, flag):
        if flag:
            self.draw(color='gray')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.func()


class Sprite_Mouse_Location(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(0, 0, 1, 1)


class UMenu:
    def __init__(self, screen, general=True):
        self.screen = screen
        self.general = general
        self.all_sprites = pygame.sprite.Group()
        self.rect = screen.get_rect()
        self.running = True
        self.wids = list()

    def mainloop(self, color='blue'):
        mouse_sprite = Sprite_Mouse_Location()
        self.draw_all()
        pygame.display.flip()
        while self.running:
            screen.fill(color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEMOTION:
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    for i in self.all_sprites:
                        i.pos_check(mouse_sprite)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    for i in self.all_sprites:
                        i.click_check(mouse_sprite)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

    def addWidget(self, wid):
        self.all_sprites.add(wid)
        self.wids.append(wid)
        return len(self.wids) - 1

    def draw_all(self):
        for wid in self.wids:
            wid.draw()

    def close(self):
        self.running = False


class ULevelsPlace(UWidget):
    def __init__(self, menu, func):
        super(ULevelsPlace, self).__init__(menu)
        self.checked = 0
        self.lvl_name = 'circle'
        self.levels = list()
        self.rows = 3
        self.cols = 3
        self.width = self.menu.rect.w
        self.height = self.menu.rect.h
        self.func = func

    def addLevel(self, image, name):
        self.levels.append((image, name))

    def draw(self):
        self.image = pygame.Surface((self.width, self.height - 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, pygame.Color('gray'), (0, 0, self.width, self.height))
        part_x = 10 if len(self.levels) == 0 else (self.rect.w - self.rows * 10 - 10) // self.rows
        self.cell_size_x = part_x
        self.cell_size_y = (self.rect.h - 10) // (self.cols)
        count = 0
        for i in range(self.rows):
            for j in range(1, self.cols + 1):
                if len(self.levels) > count:
                    image_lvl = self.levels[count][0]
                    lvl_name = self.levels[count][1]
                    pygame.draw.rect(self.image, pygame.Color('red'), (10 * j + part_x * (j - 1),
                                                                       10 + (i * self.rect.h + 10) // (self.cols) - 10,
                                                                       part_x,
                                                                       (self.rect.h - 10) // (self.cols)),
                                     border_radius=20)
                    cookie_img = load_image('universla_cookie.png')
                    cookie_img = pygame.transform.scale(cookie_img, (part_x, (self.rect.h - 100) // (self.cols)))
                    self.image.blit(cookie_img,
                                    (10 * j + part_x * (j - 1),
                                     10 + (i * self.rect.h + 10) // (self.cols)))
                    image_lvl = pygame.transform.scale(image_lvl,
                                                       (part_x,
                                                        (self.rect.h - 100) // (self.cols)))
                    self.image.blit(image_lvl,
                                    (10 * j + part_x * (j - 1),
                                     10 + (i * self.rect.h + 10) // (self.cols)))

                    font = pygame.font.Font(pygame.font.match_font('calibri'), 20)
                    text_pg = font.render(f'{lvl_name}', True, (0, 0, 0))
                    self.image.blit(text_pg, (10 + 10 * (j + 1) + part_x * (j - 1),
                                              (((i + 1) * self.rect.h + 10) // (self.cols)) - text_pg.get_height()))
                    count += 1

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            cell_x = (pos.rect.x - 10) // self.cell_size_x
            cell_y = (pos.rect.y - 10) // self.cell_size_y
            if cell_x < 0 or cell_x >= self.rows or cell_y < 0 or cell_y >= self.cols:
                return
            self.func(self.levels[(cell_x * self.rows) + cell_y][0])
        self.draw()

    def change_size(self, width, height):
        self.width = width
        self.height = height


class UMusicButton(UWidget):
    def __init__(self, menu):
        super(UMusicButton, self).__init__(menu)
        self.music_is = False

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image('music.png', -1), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.menu.rect.h - self.rect.h - 10
        if self.music_is:
            pygame.draw.line(self.image, pygame.Color('red'), (100, 0), (0, 100), 10)

    def hover(self, flag):
        if flag:
            self.draw(color='gray')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.music_is = not self.music_is


class UBackButton(UWidget):
    def __init__(self, menu, pos):
        super(UBackButton, self).__init__(menu)
        self.pos = pos

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image('back.png', -1), (self.pos[2], self.pos[3]))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'black', self.pos)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.menu.close()


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    levels_place.addLevel(load_image('star4.png', -1), 'star')
    back_btn = UBackButton(menu_lvl, (0, 450, 700, 50))
    menu_lvl.mainloop('gray')


def start_the_game(lvl_name):
    print('ЗАПУСКАЕМ ВУХУУУУУ')


pygame.init()
width, height = 700, 500
screen = pygame.display.set_mode((width, height))
menu = UMenu(screen)
button = UButton(menu, go_to_levels, text='start')
button2 = UMusicButton(menu)
pygame.display.flip()
menu.mainloop()