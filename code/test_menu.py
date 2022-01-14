import sys

import pygame
from game_view import game_run
from support_funcs import load_image, get_levels
from UT import UMenu, ULevelsPlace, UBackButton, UButton, UMusicButton


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2, color='Gray', transparent=False)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    for name, res, time in get_levels():
        if res is None:
            levels_place.addLevel(load_image(fr'..\images\{name}.png', -1), f'{name}', name)
        else:
            levels_place.addLevel(load_image(fr'..\images\{name}.png', -1), f'{name}, {res}%, {time}sec', name)
    UBackButton(menu_lvl, (0, 450, 50, 50), menu_lvl.close)
    menu_lvl.mainloop()


def start_the_game(lvl_name, menu1):
    game_run(lvl_name, menu1, not msc_btn.music_is)


def main():
    pygame.init()
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    menu = UMenu(screen)
    menu.setFon(load_image('../ui_images/fon.jpg'))
    sound2 = pygame.mixer.Sound('../sound/intro_music.wav')
    sound2.play()
    UButton(menu, go_to_levels, 'start', 0)
    global msc_btn
    msc_btn = UMusicButton(menu, [sound2.play, sound2.stop])
    UButton(menu, [sys.exit], 'quit', 1)
    pygame.display.flip()
    menu.mainloop()


if __name__ == '__main__':
    main()
