import os
import sys
import pygame

size = width, height = 700, 500
screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('white'))


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
    image = load_image("good_circle.png", -1)

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
        if not pygame.sprite.collide_mask(self, star_form):
            print("Проиграл")


all_sprites = pygame.sprite.Group()
drawed = pygame.sprite.Group()
running = True
clock = pygame.time.Clock()
cookie = Cookie()
star_form = Form()
all_poses = set()
pygame.display.set_caption("PySquid")
while running:
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
                print(len(xs), len(ys))
    all_sprites.update()
    screen.fill(pygame.Color('grey'))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()