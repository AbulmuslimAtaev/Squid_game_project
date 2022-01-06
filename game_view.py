import os
import sys
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


class Check_Form(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        # self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x = (width - 200) // 2 + pos[0] * 4 - 1
        self.rect.y = (height - 200) // 2 + pos[1] * 4 - 1


def draw_update():
    for i in drawed_check.sprites():
        if not pygame.sprite.spritecollideany(i, drawed):
            return False
    return True


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
pygame.display.set_caption("PySquid")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    press = pygame.mouse.get_pressed()
    if press[0]:
        pos = pygame.mouse.get_pos()
        drawed.add(Spot(pos))
        drawed.update()
        if draw_update():
            running = False
    all_sprites.update()
    screen.fill(pygame.Color('grey'))
    all_sprites.draw(screen)
    drawed_check.draw(screen)
    pygame.display.flip()
if not running:
    print("Победа")
pygame.quit()
