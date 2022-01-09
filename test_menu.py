import game_view
from UT import *


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    levels_place.change_size(700, 450)
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    levels_place.addLevel(load_image('star4.png', -1), 'star4')
    back_btn = UBackButton(menu_lvl, (0, 450, 700, 50), main)
    menu_lvl.mainloop('gray')


def start_the_game(lvl_name, menu):
    game_view.game_run(lvl_name, menu)

def main():
    pygame.init()
    width, height = 700, 500
    screen = pygame.display.set_mode((width, height))
    menu = UMenu(screen)
    button = UButton(menu, go_to_levels, 'start', 0)
    button2 = UMusicButton(menu)
    pygame.display.flip()
    menu.mainloop()


if __name__ == '__main__':
    main()