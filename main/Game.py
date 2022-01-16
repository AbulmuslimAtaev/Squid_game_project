from UT import UMenu, UPauseButton
from dbManager import dbManager
from SupportFuncs import *
from MySprites import *


class Game:
    def __init__(self, image_name, menu=None, music_is=True):
        pygame.init()
        self.size = (700, 500)
        self.screen = pygame.display.set_mode(self.size)

        self.image_name = image_name
        self.menu = menu
        self.music_is = music_is

        self.running = True
        self.pause_flag = False
        self.win_flag = False

        self.all_sprites = pygame.sprite.Group()

        self.font = pygame.font.Font('../font/arial.ttf', 50)

        self.MYEVENTTYPE = pygame.USEREVENT + 1
        self.MYEVENTTYPE2 = pygame.USEREVENT + 2
        pygame.time.set_timer(self.MYEVENTTYPE2, 100)
        self.MYEVENTTYPE3 = pygame.USEREVENT + 3
        pygame.time.set_timer(self.MYEVENTTYPE3, 500)

        self.process = 0

        self.db_manager = dbManager('../data/database.sqlite')

        self.time_str = '0.001'

    def music_go(self):
        if self.music_is:
            pygame.display.set_caption("PySquid")
            pygame.mixer.music.load('../sound/game_musik.ogg')
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play(-1)

            sound1 = pygame.mixer.Sound('../sound/crackling.wav')
            pygame.mixer.Channel(0).set_volume(0.4)
            pygame.mixer.Channel(0).play(sound1, loops=-1)
            pygame.mixer.Channel(0).pause()
            pygame.time.set_timer(self.MYEVENTTYPE, 50)

    def run(self):
        self.music_go()

        drawed_check = pygame.sprite.Group()
        drawed = pygame.sprite.Group()
        igla_sprites = pygame.sprite.Group()
        values = pic2text(self.image_name)
        count_of_values = 0
        for i in values[0]:
            CheckForm(i, drawed_check, self.size)
            count_of_values += 1
        Cookie(self.all_sprites, self.size)
        form = Form(values[1], self.image_name, self.all_sprites, self.size)
        self.menu.transparent = False

        pause = self.make_me_pause()

        igla = Igla(igla_sprites, self.size)
        mouse_sprite = SpriteMouseLocation()

        igla_flag = False
        time = float(self.time_str)
        flag = False, count_of_values
        if len(str(round(time))) <= 1:
            self.time_str = "0" + self.time_str
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == self.MYEVENTTYPE:
                    igla_flag = True
                if event.type == self.MYEVENTTYPE2:
                    time = round(time + 0.1, 2)
                if event.type == self.MYEVENTTYPE3:
                    self.db_manager.set_data('levels_result',
                                             {'result': self.process, 'time': self.time_str},
                                             {'level_name =': f"'{self.image_name}'", 'result <': self.process})
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_is:
                        pygame.mixer.Channel(0).unpause()
                    mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
                    self.pause_flag = pause.click_check(mouse_sprite)
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.music_is:
                        pygame.mixer.Channel(0).pause()
            press = pygame.mouse.get_pressed()
            pos = pygame.mouse.get_pos()
            if press[0]:
                if not self.pause_flag:
                    if igla_flag:
                        igla.turn()
                        igla_flag = False
                    spot = Spot(pos, drawed)
                    if spot.check_lose(form):
                        self.running = False
                        self.win_flag = False
                    flag = draw_update(drawed_check, drawed)
                    if self.process == 100:
                        self.running = False
                        self.win_flag = True

            self.screen.fill(pygame.Color('grey'))
            self.all_sprites.draw(self.screen)
            drawed.draw(self.screen)
            igla_sprites.draw(self.screen)
            drawed_check.draw(self.screen)

            if pygame.mouse.get_focused():
                pygame.mouse.set_visible(False)
                igla.move(pos)

            self.time_str = str(time) + "0"
            if len(str(round(time))) <= 1:
                self.time_str = "0" + self.time_str
            self.process = 100 - flag[1] * 100 // count_of_values
            self.draw_time_and_process(self.time_str, self.process)
            pygame.display.flip()
        if not self.running and not self.pause_flag:
            pygame.mixer.Channel(0).pause()

    def draw_time_and_process(self, time, proc):
        text_pg = self.font.render(time, True, (0, 0, 0))
        self.screen.blit(text_pg, (self.size[0] * 3 // 4 - text_pg.get_width() // 2,
                                   self.size[1] // 8 * 7 - text_pg.get_height() // 2))
        text_pg = self.font.render(f"{proc}%", True, (0, 0, 0))
        buff_text_pg = self.font.render(f"{proc}", True, (0, 0, 0))
        self.screen.blit(text_pg, (self.size[0] // 2 - buff_text_pg.get_width() // 2,
                                   self.size[1] // 10))

    def close(self):
        self.running = False

    def make_me_pause(self):
        pause = UPauseButton(self.all_sprites, None, self.screen)
        pause.set_gen_menu([pause.menu.close, self.close, pygame.mixer.music.stop])
        pause.addButton('Resume', pause.menu.close)
        pause.addButton('Quit', sys.exit)
        return pause


if __name__ == '__main__':
    game = Game('lighting', UMenu)
    game.run()