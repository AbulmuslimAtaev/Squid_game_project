import os
import sys
import pygame

size = width, height = 400, 400
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
    image = load_image("star_form.png", -1)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Form.image
        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 40
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)


class Cookie(pygame.sprite.Sprite):
    image = load_image("universla_cookie.png")

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Cookie.image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (400, 400))


all_sprites = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()
cookie = Cookie()
star_form = Form()
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(event.pos)
    all_sprites.update()
    screen.fill(pygame.Color('blue'))
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()