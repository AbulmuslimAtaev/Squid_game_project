import sys
import pygame
from SupportFuncs import load_image
from dbManager import dbManager
from UT import UMenu, ULevelsPlace, UBackButton, UButton, UMusicButton, UFinalWindow
from Game import Game


def go_to_levels():
    screen2 = pygame.display.set_mode((700, 500))
    menu_lvl = UMenu(screen2, color='Gray', transparent=False)
    menu_lvl.changeMouseConstantToClick(pygame.MOUSEBUTTONDOWN)
    levels_place = ULevelsPlace(menu_lvl, start_the_game)
    update_levels(levels_place)
    levels_place.add_update_levels(update_levels)
    levels_place.change_size(700, 450)
    UBackButton(menu_lvl, (0, 450, 50, 50), menu_lvl.close)
    menu_lvl.mainloop()


def update_levels(levels_place):
    db_manager = dbManager('../data/database.sqlite')
    for name, res, time in db_manager.get_data('levels_result', '*', ''):
        if res == 0:
            levels_place.addLevel(load_image(fr'../images/{name}.png', -1), f'{name}', name)
        else:
            levels_place.addLevel(load_image(fr'../images/{name}.png', -1), f'{name}, {res}%, {round(float(time))}s',
                                  name)


def start_the_game(lvl_name, menu):
    game = Game(lvl_name, menu, not msc_btn.music_is)
    game.run()
    db_manager = dbManager('../data/database.sqlite')
    final_win = UFinalWindow(game.all_sprites, menu.screen)
    final_win.addButton('Back', [final_win.menu.close, pygame.mixer.music.stop])
    final_win.addButton('Quit', sys.exit)
    final_win.addLabel(f'{game.process}% | {game.time_str}s', (350, 180), (153, 204, 51))
    if game.win_flag and not game.pause_flag:
        db_manager.update_data('levels_result', {'result': 100, 'time': game.time_str},
                               {'level_name = ': f'"{lvl_name}"'})
        final_win.menu.setFon(load_image('../ui_images/WinPlace.png'))
        final_win.go()
    elif not game.pause_flag:
        final_win.menu.setFon(load_image('../ui_images/LosePlace.png'))
        final_win.go()


def main():
    pygame.init()
    pygame.display.set_caption("PySquid")
    icon = pygame.image.load("../ui_images/icon.png")
    pygame.display.set_icon(icon)
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
    try:
        main()
    except SystemExit:
        sys.exit(0)
