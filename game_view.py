import os
import sys
import pygame


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
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
        self.image = load_image("universla_cookie.png")
        self.image = pygame.transform.scale(self.image, (300, 300))
        self.rect = self.image.get_rect()
        print(self.image.get_at((150, 150)))
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
        if not pygame.sprite.collide_mask(self, form):
            print("Проиграл")


size = width, height = 700, 500
FPS = 60


def game_run(level):
    drawed = pygame.sprite.Group()
    clock = pygame.time.Clock()

    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    all_poses = set()
    pygame.display.set_caption("PySquid")

    global all_sprites
    global cookie
    global form

    all_sprites = pygame.sprite.Group()
    cookie = Cookie()
    form = Form(level)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        press = pygame.mouse.get_pressed()
        if press[0]:
            pos = pygame.mouse.get_pos()
            if pos not in all_poses:
                all_poses.add(pos)
                spot = Spot(pos)
                drawed.add(spot)
                drawed.update()
                xs = [i[0] for i in all_poses]
                ys = [i[1] for i in all_poses]

                if len(xs) > 544 and len(ys) > 544:
                    print('Победа')
                    return
        all_sprites.update()
        screen.fill(pygame.Color('grey'))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    game_run('lightning')