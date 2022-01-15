import sqlite3

import pygame
from random import randint
import sys
from itertools import cycle
from UT import UMenu, UPauseButton, UFinalWindow
from support_funcs import SpriteMouseLocation, pic2text, load_image

pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)


class Igla(pygame.sprite.Sprite):
    images = [load_image(fr"..\images\animation\pic{i}.png", None) for i in range(0, 17)]

    def __init__(self, group, size):
        super().__init__(group)
        self.num = cycle(list(range(0, 17)) + (list(range(16, -1, -1))))
        for i in range(8):
            next(self.num)
        self.image = Igla.images[next(self.num)]
        self.rect = self.image.get_rect()
        self.rect.x = (size[0] - self.rect.w) // 2
        self.rect.y = (size[1] - self.rect.h) // 2

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def turn(self):
        self.image = Igla.images[next(self.num)]


class Form(pygame.sprite.Sprite):
    def __init__(self, image, image2, group, size):
        super().__init__(group)
        self.image = load_image(image, -1, False)
        print(f"{image2}")
        self.image1 = load_image(f"../images/{image2}.png", -1)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image1 = pygame.transform.scale(self.image1, (200, 200))
        self.rect = self.image.get_rect()
        # self.image, self.image1 = self.image1, self.image
        self.rect.x = (size[0] - self.rect.w) // 2
        self.rect.y = (size[1] - self.rect.h) // 2
        self.mask = pygame.mask.from_surface(self.image1)


class Cookie(pygame.sprite.Sprite):
    image = load_image(r"../images/cookie.png")

    def __init__(self, group, size):
        super().__init__(group)
        self.image = Cookie.image
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = (size[0] - self.rect.w) // 2
        self.rect.y = (size[1] - self.rect.h) // 2


class Spot(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("grey"), (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 2
        self.rect.y = pos[1] - 2

    def check_lose(self, sprite_to_check):
        if not pygame.sprite.collide_mask(self, sprite_to_check):
            return True


class CheckForm(pygame.sprite.Sprite):
    def __init__(self, pos, group, size):
        super().__init__(group)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        # self.image.fill((0, 0, 0))
        self.rect.x = (size[0] - 200) // 2 + pos[0] * 2 - 1
        self.rect.y = (size[1] - 200) // 2 + pos[1] * 2 - 1


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


class Game:
    def __init__(self, image_name, menu=None, music_is=True):
        self.image_name = image_name
        self.menu = menu
        self.music_is = music_is

        self.running = True
        self.pause_flag = False
        self.win_flag = False

        self.all_sprites = pygame.sprite.Group()

        self.con = sqlite3.connect("../data/database.sqlite")
        self.cur = self.con.cursor()

        self.font = pygame.font.SysFont('Consolas', 30)

        self.MYEVENTTYPE = pygame.USEREVENT + 1
        self.MYEVENTTYPE2 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.MYEVENTTYPE2, 100)
        self.MYEVENTTYPE3 = pygame.USEREVENT + 3
        pygame.time.set_timer(self.MYEVENTTYPE3, 500)

    def music_go(self):
        if self.music_is:
            pygame.display.set_caption("PySquid")
            pygame.mixer.music.load('../sound/game_musik.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

            sound1 = pygame.mixer.Sound('../sound/crackling.wav')
            pygame.mixer.Channel(0).set_volume(0.4)
            pygame.mixer.Channel(0).play(sound1, loops=-1)
            pygame.mixer.Channel(0).pause()
            pygame.time.set_timer(self.MYEVENTTYPE, 50)

    def run(self):
        self.music_go()

        drawed_check = pygame.sprite.Group()
        drawed = pygame.sprite.Group()
        igla_sprites = pygame.sprite.Group()
        values = pic2text(self.image_name)
        count_of_values = 0
        for i in values[0]:
            CheckForm(i, drawed_check, size)
            count_of_values += 1
        Cookie(self.all_sprites, size)
        form = Form(values[1], self.image_name, self.all_sprites, size)
        self.menu.transparent = False

        pause = self.make_me_pause()

        igla = Igla(igla_sprites, size)
        mouse_sprite = SpriteMouseLocation()

        igla_flag = False
        time = 0.001
        flag = False, count_of_values
        process = 0
        self.time_str = str(time)
        if len(str(round(time))) <= 1:
            self.time_str = "0" + self.time_str
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == self.MYEVENTTYPE:
                    igla_flag = True
                if event.type == self.MYEVENTTYPE2:
                    time = round(time + 0.1, 2)
                if event.type == self.MYEVENTTYPE3:
                    req = f"UPDATE Levels_rezult SET rezult = {process}, time = '{self.time_str}' WHERE Level_name = '{self.image_name}' AND {process} > rezult"
                    print(req)
                    self.cur.execute(req)
                    self.con.commit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_is:
                        pygame.mixer.Channel(0).unpause()
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    self.pause_flag = pause.click_check(mouse_sprite)
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.music_is:
                        pygame.mixer.Channel(0).pause()
            press = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            if press[0]:
                if not self.pause_flag:
                    if igla_flag:
                        igla.turn()
                        igla_flag = False
                    spot = Spot(pos, drawed)
                    if spot.check_lose(form):
                        self.running = False
                        self.win_flag = False
                    flag = draw_update(drawed_check, drawed)
                    if process == 100:
                        self.running = False
                        self.win_flag = True

            screen.fill(pygame.Color('grey'))
            self.all_sprites.draw(screen)
            drawed.draw(screen)
            igla_sprites.draw(screen)
            drawed_check.draw(screen)

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                igla.move(pos)

            self.time_str = str(time) + "0"
            if len(str(round(time))) <= 1:
                self.time_str = "0" + self.time_str
            process = 100 - flag[1] * 100 // count_of_values
            self.draw_time_and_process(self.time_str, process)

            pygame.display.flip()
        if not self.running and not self.pause_flag:
            pygame.mixer.Channel(0).pause()

    def draw_time_and_process(self, time, proc):
        screen.blit(self.font.render(time,
                                     True, (0, 0, 0)), (size[0] * 3 // 4, size[1] // 8 * 7))
        screen.blit(self.font.render(f"{proc}%",
                                     True, (0, 0, 0)), (size[0] * 2 // 4 - 15, size[1] // 10))

    def close(self):
        self.running = False

    def make_me_pause(self):
        pause = UPauseButton(self.all_sprites, None, screen)
        pause.set_gen_menu([pause.menu.close, self.close, pygame.mixer.music.stop])
        pause.addButton('Resume', pause.menu.close)
        pause.addButton('Quit', sys.exit)
        return pause


if __name__ == '__main__':
    print('hi')
    game = Game('lighting', UMenu)
    game.run()
