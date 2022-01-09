import pygame
from random import randint
import sys
from itertools import cycle
from UT import UMenu, UBackButton, UPauseMenu
from support_funcs import SpriteMouseLocation, pic2text, load_image

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))


class PauseButton(pygame.sprite.Sprite):
    def __init__(self, group, gen_menu):
        super(PauseButton, self).__init__(group)
        self.image = pygame.transform.scale(load_image(r'..\images\pause.png'), (50, 50))
        self.rect = self.image.get_rect()
        self.gen_menu = gen_menu

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.go_to_pause()
            return True

    def go_to_pause(self):
        menu = UMenu(screen)
        back_btn = UBackButton(menu, (600, 400, 100, 100))
        ps_menu = UPauseMenu(menu)
        ps_menu.addButton('Resume', self.gen_menu.mainloop)
        ps_menu.addButton('Quit', pygame.quit)
        menu.mainloop(False)


class Igla(pygame.sprite.Sprite):
    images = [load_image(fr"..\images\animation\pic{i}.png", None) for i in range(0, 17)]

    def __init__(self, group):
        super().__init__(group)
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


class Form(pygame.sprite.Sprite):
    def __init__(self, image_name, group):
        super().__init__(group)
        self.image = load_image(f"{image_name}.png", -1)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2
        self.mask = pygame.mask.from_surface(self.image)


class Cookie(pygame.sprite.Sprite):
    image = load_image(r"..\images\cookie.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Cookie.image
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2


class Spot(pygame.sprite.Sprite):
    def __init__(self, pos, group, sprite_to_check):
        super().__init__(group)
        self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("grey"), (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 2
        self.rect.y = pos[1] - 2
        if not pygame.sprite.collide_mask(self, sprite_to_check):
            print("Проиграл")


class checkForm(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = (width - 200) // 2 + pos[0] * 2 - 1
        self.rect.y = (height - 200) // 2 + pos[1] * 2 - 1


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
    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 50)

    all_sprites = pygame.sprite.Group()
    drawed_check = pygame.sprite.Group()
    drawed = pygame.sprite.Group()
    igla_sprites = pygame.sprite.Group()

    values = pic2text(image_name)
    for i in values:
        checkForm(i, drawed_check)

    Cookie(all_sprites)
    form = Form(image_name, all_sprites)
    pause = PauseButton(all_sprites, menu)
    igla = Igla(igla_sprites)
    mouse_sprite = SpriteMouseLocation()

    igla_flag = False
    running = True
    pause_flag = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == MYEVENTTYPE:
                igla_flag = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                pause_flag = pause.click_check(mouse_sprite)

        press = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if press[0]:
            if not pause_flag:
                if igla_flag:
                    igla.turn()
                    igla_flag = False
                Spot(pos, drawed, form)
                if draw_update(drawed_check, drawed):
                    running = False

        screen.fill(pygame.Color('grey'))
        all_sprites.draw(screen)
        drawed.draw(screen)
        igla_sprites.draw(screen)

        if pygame.mouse.get_focused():
            pygame.mouse.set_visible(False)
            igla.move(pos)

        pygame.display.flip()
    if not running:
        print("Победа")

    if menu:
        menu.close()
    else:
        sys.exit()


if __name__ == '__main__':
    game_run(r'..\images\star4', None)
