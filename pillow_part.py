from PIL import Image

im = Image.open(r'images\lightning.png')


pixels = im.load()
x, y = im.size
with open('files/lightning.txt', 'w', encoding='utf-8') as f:
    for i in range(x):
        for j in range(y):
            if pixels[i, j] == (0, 0, 0):
                print(f'{i};{j}', end=' ', file=f)


# import pygame
# import sys


# pygame.init()
# screen = pygame.display.set_mode((500, 500))
# screen.fill(pygame.Color('white'))
# print(help(pygame.draw.circle))
# for i in range(len(pixs)):
#     pygame.draw.circle(screen, (0, 0, 0), pixs[i], 5)
# pygame.display.flip()
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
