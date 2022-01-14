import pygame
from game_view import game_run
from support_funcs import load_image
from UT import UMenu, ULevelsPlace, UBackButton, UButton, UMusicButton


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2, color='Purple', transparent=True)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    levels_place.addLevel(load_image(r'..\images\triangle.png', -1), 'triangle')
    levels_place.addLevel(load_image(r'..\images\circle.png', -1), 'circle')
    levels_place.addLevel(load_image(r'..\images\sueta.png', -1), 'sueta')
    levels_place.addLevel(load_image(r'..\images\star4.png', -1), 'star4')
    levels_place.addLevel(load_image(r'..\images\heart.png', -1), 'heart')
    levels_place.addLevel(load_image(r'..\images\star5.png', -1), 'star5')
    levels_place.addLevel(load_image(r'..\images\star6.png', -1), 'star6')
    levels_place.addLevel(load_image(r'..\images\lighting.png', -1), 'lighting')
    levels_place.addLevel(load_image(r'..\images\cloud.png', -1), 'cloud')
    UBackButton(menu_lvl, (0, 450, 50, 50), main)
    menu_lvl.mainloop()


def start_the_game(lvl_name, menu):
    game_run(lvl_name, menu)


def main():
    pygame.init()
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    menu = UMenu(screen)
    menu.setFon(load_image('../ui_images/fon.jpg'))
    UButton(menu, go_to_levels, 'start', 0)
    UMusicButton(menu)
    pygame.display.flip()
    menu.mainloop()


if __name__ == '__main__':
    main()
