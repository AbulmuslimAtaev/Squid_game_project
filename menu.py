import pygame
import pygame_menu
from game_view import game_run


level = 'lightning'


def set_level(*value):
    print(value)
    global level
    level = value[0][0][0]


def start_the_game():
    game_run(level)


pygame.init()
surface = pygame.display.set_mode((700, 500))
menu = pygame_menu.Menu('PySquid', 700, 500, theme=pygame_menu.themes.THEME_DARK)

menu.add.selector('Level :', [('lightning', 1), ('circle', 2)], onchange=set_level)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)