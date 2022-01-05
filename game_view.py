import os
import random
import sys
import pygame


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


class Form(pygame.sprite.Sprite):

    def __init__(self, level):
        super().__init__(all_sprites)
        self.image = load_image(level + '.png', -1)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = load_image("cookie3.png", -1)
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        print(self.image.get_at((150, 150)))
        self.rect.x = (width - self.rect.w) // 2
        self.rect.y = (height - self.rect.h) // 2


class Part(pygame.sprite.Sprite):
    flag = 1
    colors = [(166, 88, 41), (184, 98, 46), (147, 77, 36), (179, 100, 54), (121, 74, 46), (92, 57, 37)]

    def __init__(self, pos):
        super(Part, self).__init__()
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        pygame.draw.circle(self.image, random.choice(Part.colors), (1, 1), 1)
        self.rect = self.image.get_rect()
        self.rect.x = 0.8 * pos[0] + width // 4 + 60
        self.rect.y = 0.8 * pos[1] + height // 4 + 20

    def update(self):
        if not pygame.sprite.spritecollideany(self, drawed):
            Part.flag = 0
        else:
            self.update = lambda: None

    def null_flag(self):
        Part.flag = 1


class Spot(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((7, 7), pygame.SRCALPHA)
        pygame.draw.circle(self.image, pygame.Color("grey"), (4, 4), 3)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0] - 2
        self.rect.y = pos[1] - 2
        if not pygame.sprite.spritecollideany(self, parts_sprites):
            print("Проиграл")


size = width, height = 700, 500


def game_run(level):
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    pygame.display.set_caption("PySquid")

    global all_sprites
    global parts_sprites
    global drawed
    global cookie
    # global form

    all_sprites = pygame.sprite.Group()
    parts_sprites = pygame.sprite.Group()
    drawed = pygame.sprite.Group()
    cookie = Cookie()
    # form = Form(level)

    with open(fr'files/{level}.txt', 'r', encoding='utf-8') as f:
        for i in f.readline().split(' '):
            if i:
                pos = tuple([int(j) for j in i.split(';')])
                part = Part(pos)
                parts_sprites.add(part)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        press = pygame.mouse.get_pressed()
        if press[0]:
            pos = pygame.mouse.get_pos()
            spot = Spot(pos)
            drawed.add(spot)
            drawed.update()
            parts_sprites.update()
            if Part.flag:
                print('ПОБЕДААААААА')
            Part.null_flag(None)
        all_sprites.update()
        screen.fill(pygame.Color('grey'))
        all_sprites.draw(screen)
        parts_sprites.draw(screen)
        drawed.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_run('circle')