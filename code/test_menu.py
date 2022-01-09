import pygame
from game_view import game_run
from support_funcs import load_image
from UT import UMenu, ULevelsPlace, UBackButton, UButton, UMusicButton


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2, color='gray', transparent=False)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\cloud.png', -1), 'cloud')
    levels_place.addLevel(load_image(r'..\images\lighting.png', -1), 'lighting')
    levels_place.addLevel(load_image(r'..\images\easy.png', -1), 'easy')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    UBackButton(menu_lvl, (0, 450, 700, 50), main)
    menu_lvl.mainloop()


def start_the_game(lvl_name, menu):
    game_run(lvl_name, menu)


def main():
    pygame.init()
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    menu = UMenu(screen)
    UButton(menu, go_to_levels, 'start', 0)
    UMusicButton(menu)
    pygame.display.flip()
    menu.mainloop()


if __name__ == '__main__':
    main()