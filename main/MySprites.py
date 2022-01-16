import pygame
from itertools import cycle
from SupportFuncs import load_image


class Igla(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.num = cycle(list(range(0, 17)) + (list(range(16, -1, -1))))
        for i in range(8):
            next(self.num)
        self.images = [load_image(fr"..\images\animation\pic{i}.png", None) for i in range(0, 17)]
        self.image = self.images[next(self.num)]
        self.rect = self.image.get_rect()
        self.rect.x = (size[0] - self.rect.w) // 2
        self.rect.y = (size[1] - self.rect.h) // 2

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def turn(self):
        self.image = self.images[next(self.num)]


class Form(pygame.sprite.Sprite):
    def __init__(self, image, image2, group, size):
        super().__init__(group)
        self.image = load_image(image, -1, False)
        self.image1 = load_image(f"../images/{image2}.png", -1)
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.image1 = pygame.transform.scale(self.image1, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.x = (size[0] - self.rect.w) // 2
        self.rect.y = (size[1] - self.rect.h) // 2
        self.mask = pygame.mask.from_surface(self.image1)


class Cookie(pygame.sprite.Sprite):
    def __init__(self, group, size):
        super().__init__(group)
        self.image = load_image(r"../images/cookie.png")
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
        self.rect.x = (size[0] - 200) // 2 + pos[0] * 2 - 1
        self.rect.y = (size[1] - 200) // 2 + pos[1] * 2 - 1