import pygame
from random import randint
import sys
from itertools import cycle
from UT import UMenu, UPauseButton, UFinalWindow
from support_funcs import SpriteMouseLocation, pic2text, load_image

pygame.init()
size = (700, 500)
screen = pygame.display.set_mode(size)
MYEVENTTYPE = pygame.USEREVENT + 1


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
    fg = True
    for i in in_group.sprites():
        if not pygame.sprite.spritecollideany(i, group_to_check):
            fg = False
        else:
            i.kill()
    if not fg:
        return False
    return True


def game_run(image_name, menu=None):
    pygame.display.set_caption("PySquid")
    pygame.mixer.music.load('../sound/game_musik.ogg')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    sound1 = pygame.mixer.Sound('../sound/crackling.wav')
    pygame.mixer.Channel(0).set_volume(0.4)
    pygame.mixer.Channel(0).play(sound1, loops=-1)
    pygame.mixer.Channel(0).pause()
    sound2 = pygame.mixer.Sound('../sound/intro_music.wav')
    pygame.time.set_timer(MYEVENTTYPE, 50)
    MYEVENTTYPE2 = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE2, 10)
    all_sprites = pygame.sprite.Group()
    drawed_check = pygame.sprite.Group()
    drawed = pygame.sprite.Group()
    igla_sprites = pygame.sprite.Group()
    values = pic2text(image_name)
    for i in values[0]:
        CheckForm(i, drawed_check, size)
    Cookie(all_sprites, size)
    form = Form(values[1], image_name, all_sprites, size)

    pause = UPauseButton(all_sprites, menu, screen)
    pause.addButton('Resume', pause.menu.close)
    pause.addButton('Quit', sys.exit)

    igla = Igla(igla_sprites, size)
    mouse_sprite = SpriteMouseLocation()

    igla_flag = False
    running = True
    pause_flag = False
    win_flag = False
    time = 0.001
    font = pygame.font.SysFont('Consolas', 30)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MYEVENTTYPE:
                igla_flag = True
            if event.type == MYEVENTTYPE2:
                time = round(time + 0.01, 2)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Channel(0).unpause()
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                pause_flag = pause.click_check(mouse_sprite)
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.mixer.Channel(0).pause()
        press = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if press[0]:
            if not pause_flag:
                if igla_flag:
                    igla.turn()
                    igla_flag = False
                spot = Spot(pos, drawed)
                if spot.check_lose(form):
                    running = False
                    win_flag = False
                if draw_update(drawed_check, drawed):
                    running = False
                    win_flag = True
        screen.fill(pygame.Color('grey'))
        all_sprites.draw(screen)
        drawed.draw(screen)
        igla_sprites.draw(screen)
        drawed_check.draw(screen)
        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            igla.move(pos)
        time_str = str(time).replace(".", ":")
        if len(str(round(time))) <= 1:
            time_str = "0" + time_str
        screen.blit(font.render(time_str,
                                True, (0, 0, 0)), (size[0] * 3 // 4, size[1] // 8))
        pygame.display.flip()
    if not running:
        pygame.mixer.Channel(0).pause()
        final_win = UFinalWindow(all_sprites, screen)
        final_win.addButton('Back', menu.mainloop)
        final_win.addButton('Quit', sys.exit)
        if win_flag:
            print("Выиграл")
            final_win.menu.setFon(load_image('../ui_images/BigPurple.png'))
        else:
            final_win.menu.setFon(load_image('../ui_images/BigPurple.png'))
            print("Проиграл")
        final_win.go()

    #
    # if menu:
    #     pygame.mouse.set_visible(True)
    #     menu.close()
    # else:
    #     sys.exit()


if __name__ == '__main__':
    game_run(r'lighting', UMenu)
