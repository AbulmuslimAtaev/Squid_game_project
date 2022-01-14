from support_funcs import SpriteMouseLocation, load_image
import pygame
import sys


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

    def click_check(self, pos):
        pass


class UButton(UWidget):
    def __init__(self, menu, func, text, num):
        super(UButton, self).__init__(menu)
        self.text = text
        self.flag = False
        self.func = func
        self.num = num

    def draw(self, image_name='BigPurple.png'):
        if self.text:
            font = pygame.font.Font(pygame.font.match_font('Arial'), 50)
            text_pg = font.render(self.text, True, (255, 255, 255))
            self.image = pygame.transform.scale(load_image('../ui_images/' + image_name), (text_pg.get_width() + 40, text_pg.get_height() + 20))

            self.rect = self.image.get_rect()
            self.rect.x = self.menu.rect.w // 2 - self.rect.w // 2
            self.rect.y = self.menu.rect.h // 2 - self.rect.h // 2 + (text_pg.get_height() + 40) * self.num
            self.image.blit(text_pg, (20, 5))

    def hover(self, flag):
        if flag:
            self.draw(image_name='BigGreen.png')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.func()


class UMenu:
    def __init__(self, screen, general=True, color="purple", transparent=False):
        self.screen = screen
        self.general = general
        self.all_sprites = pygame.sprite.Group()
        self.rect = screen.get_rect()
        self.wids = list()
        self.color = color
        self.transparent = transparent
        self.MOUSECONSTANT = pygame.MOUSEBUTTONUP
        self.fon = False

    def mainloop(self):
        self.running = True
        mouse_sprite = SpriteMouseLocation()
        self.draw_all()
        pygame.display.flip()
        yes_flag = False
        while self.running:
            if not self.transparent:
                self.screen.fill(self.color)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    yes_flag = True
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    for i in self.all_sprites:
                        i.pos_check(mouse_sprite)
                elif event.type == self.MOUSECONSTANT:
                    if yes_flag:
                        mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                        for i in self.all_sprites:
                            i.click_check(mouse_sprite)
            if self.fon:
                self.screen.blit(pygame.transform.scale(self.fon, (self.rect.w, self.rect.h)), (0, 0))
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

    def changeMouseConstantToClick(self, const):
        self.MOUSECONSTANT = const

    def setFon(self, image):
        self.fon = image


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
        self.cell_size_y = (self.rect.h - 10) // self.cols
        count = 0
        for i in range(self.rows):
            for j in range(1, self.cols + 1):
                if len(self.levels) > count:
                    image_lvl = self.levels[count][0]
                    lvl_name = self.levels[count][1]
                    self.image.blit(pygame.transform.scale(load_image('../ui_images/BigPurple.png'),
                                                           (part_x, (self.rect.h - 10) // self.cols)),
                                    ((10 * j + part_x * (j - 1),10 + (i * self.rect.h + 10) // self.cols - 10)))
                    cookie_img = load_image(r'..\images\cookie.png')
                    cookie_img = pygame.transform.scale(cookie_img, (part_x, (self.rect.h - 100) // self.cols))
                    self.image.blit(cookie_img,
                                    (10 * j + part_x * (j - 1),
                                     10 + (i * self.rect.h + 10) // self.cols))
                    image_lvl = pygame.transform.scale(image_lvl,
                                                       (part_x // 2,
                                                        (self.rect.h - 100) // self.cols // 2))
                    self.image.blit(image_lvl,
                                    (10 * j + part_x * (j - 1) + image_lvl.get_width() // 2,
                                     10 + (i * self.rect.h + 10) // self.cols + image_lvl.get_height() // 2))

                    font = pygame.font.Font(pygame.font.match_font('calibri'), 20)
                    text_pg = font.render(f'{lvl_name}', True, (0, 0, 0))
                    self.image.blit(text_pg, (10 + 10 * (j + 1) + part_x * (j - 1),
                                              (((i + 1) * self.rect.h + 10) // self.cols) - text_pg.get_height()))
                    count += 1

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            cell_x = (pos.rect.x - 10) // self.cell_size_x
            cell_y = (pos.rect.y - 10) // self.cell_size_y
            if cell_x < 0 or cell_x >= self.rows or cell_y < 0 or cell_y >= self.cols:
                return
            self.func('../images/' + self.levels[(cell_y * self.rows) + cell_x][1], self.menu)

    def change_size(self, width, height):
        self.width = width
        self.height = height


class UMusicButton(UWidget):
    def __init__(self, menu, funcs):
        super(UMusicButton, self).__init__(menu)
        self.music_is = False
        self.funcs = funcs

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image(r'..\ui_images\ButtonsStyle10_05.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = self.menu.rect.h - self.rect.h - 10
        self.music_stat_draw()

    def hover(self, flag):
        if flag:
            self.draw(color='gray')
        else:
            self.draw()

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.music_is = not self.music_is
        self.music_stat_draw()

    def music_stat_draw(self):
        if self.music_is:
            self.funcs[1]()
            pygame.draw.line(self.image, pygame.Color('red'), (100, 0), (0, 100), 10)
        else:
            self.funcs[0]()


class UBackButton(UWidget):
    def __init__(self, menu, pos, gen_menu):
        super(UBackButton, self).__init__(menu)
        self.pos = pos
        self.gen_menu = gen_menu

    def draw(self, color='black'):
        self.image = pygame.transform.scale(load_image(r'..\ui_images\ButtonsStyle1_04.png', -1), (self.pos[2], self.pos[3]))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, 'black', self.pos)
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.gen_menu()


class UPauseMenu(UWidget):
    def __init__(self, menu):
        super(UPauseMenu, self).__init__(menu)
        self.buttons = list()
        self.fon = False

    def draw(self):
        if self.fon:
            self.image = load_image('../ui_images/BigPurple.png')
        else:
            self.image = pygame.Surface((300, 100 * len(self.buttons) + 100), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = self.menu.rect.w // 2 - self.rect.w // 2
        self.rect.y = self.menu.rect.h // 2 - self.rect.h // 2
        # pygame.draw.rect(self.image, (255, 200, 200), (self.menu.rect.x // 2, self.menu.rect.y // 2, 300, 100 * len(self.buttons) + 100), border_radius=20)

    def addButton(self, text, func):
        btn = UButton(self.menu, func, text, len(self.buttons))
        self.buttons.append(btn)

    # def update_max_text(self):
    #     try:
    #         print(max(self.buttons, key=lambda x: x.rect.x))
    #     except Exception:
    #         print('#')


class UPauseButton(pygame.sprite.Sprite):
    def __init__(self, group, gen_menu, screen):
        super(UPauseButton, self).__init__(group)
        self.image = pygame.transform.scale(load_image(r'..\ui_images\ButtonsStyle10_02.png'), (100, 100))
        self.rect = self.image.get_rect()
        self.gen_menu = gen_menu
        self.screen = screen
        self.buttons = list()
        self.menu = UMenu(self.screen, transparent=True)

    def click_check(self, pos):
        if pygame.sprite.collide_rect(pos, self):
            self.go_to_pause()
            return True

    def go_to_pause(self):
        UBackButton(self.menu, (600, 400, 100, 100), self.gen_menu.mainloop)
        pygame.mixer.Channel(0).pause()
        ps_menu = UPauseMenu(self.menu)
        for text, func in self.buttons:
            ps_menu.addButton(text, func)
        pygame.mouse.set_visible(True)
        self.menu.mainloop()

    def addButton(self, text, func):
        self.buttons.append((text, func))


class UFinalWindow(pygame.sprite.Sprite):
    def __init__(self, group, screen):
        super(UFinalWindow, self).__init__(group)
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.buttons = list()
        self.screen = screen
        self.menu = UMenu(self.screen, color='gray')

    def addButton(self, text, func):
        self.buttons.append((text, func))

    def go(self):
        ps_menu = UPauseMenu(self.menu)
        for text, func in self.buttons:
            ps_menu.addButton(text, func)
        pygame.mouse.set_visible(True)
        self.menu.changeMouseConstantToClick(pygame.MOUSEBUTTONDOWN)
        self.menu.mainloop()
