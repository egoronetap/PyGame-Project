# Anfisa
import sqlite3
import pygame
from constants2 import *
from my_functions import load_image, terminate, game_font


class Choice:
    def __init__(self):
        self.donebtn_info = self.create_done_btn()
        self.btns = []

    def create_done_btn(self):
        text = game_font(WIDTH // 19, 'Segoe script').render("Готово", True, (255, 255, 255))
        x, y = SIDE - text.get_width() - 50, 635
        width, height = text.get_width() + 24, text.get_height() + 4
        return [text, x, y, width, height]

    def get_click(self, mouse_pos):
        btn = self.get_btn(mouse_pos)
        done = self.on_click(btn)
        return done

    def get_btn(self, mouse_pos):
        text, x, y, width, height = list(self.donebtn_info)
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            return (x, y, width, height), 'done'
        for btn in self.btns:
            if btn[2] and btn[0][0] <= mouse_pos[0] <= btn[0][0] + btn[0][2] and \
                    btn[0][1] <= mouse_pos[1] <= btn[0][1] + btn[0][3]:
                return btn
        return None

    def on_click(self, btn):
        pass


class BackgroundChoice(Choice):
    def __init__(self, username):
        super().__init__()
        cn = sqlite3.connect(DB)
        self.backgrs = list(cn.cursor().execute(f"SELECT river, asia, forest, green_street, house, idk, leaves, "
                                                f"mountain, sky, night_forest, night_water, "
                                                f"romantic_forest, street, sunset, sunrise FROM results "
                                                f"WHERE name='{username}'").fetchall()[0])
        self.backgrs.insert(0, 1)
        self.backgr_imgs = ['space', 'river', 'asia', 'forest', 'green_street', 'house', 'idk', 'leaves', 'mountain',
                            'sky', 'night_forest', 'night_water', 'romantic_forest', 'street', 'sunset', 'sunrise']
        cn.close()
        self.sprites = self.chosen_backgr = None

    def render(self, screen):
        if not self.sprites:
            self.create_sprites()
        self.sprites.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        if self.chosen_backgr:
            pygame.draw.rect(screen, (76, 187, 23), self.chosen_backgr[0], 3)

    def create_sprites(self):
        self.sprites = pygame.sprite.Group()
        side, space = SIDE * 0.187, SIDE * 0.028
        for i in range(4):
            for j in range(4):
                if self.backgrs[i + 4 * j]:
                    img = load_image(f'{self.backgr_imgs[i + 4 * j]}.jpg')
                else:
                    img = load_image(f'clock.png', -1)
                sprite = pygame.sprite.Sprite()
                sprite.image = pygame.transform.scale(img, (side, side))
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = SIDE * 0.06 + space * (i + 1) + side * i
                sprite.rect.y = space * (j + 1) + side * j
                self.sprites.add(sprite)
        return

    def get_btn(self, mouse_pos):
        text, x, y, width, height = list(self.donebtn_info)
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            return (x, y, width, height), 'done'
        side, space = SIDE * 0.187, SIDE * 0.028
        for i in range(4):
            x = SIDE * 0.06 + space * (i + 1) + side * i
            for j in range(4):
                y = space * (j + 1) + side * j
                if self.backgrs[i + 4 * j] and x <= mouse_pos[0] <= x + side and \
                        y <= mouse_pos[1] <= y + side and self.backgrs[i + 4 * j]:
                    return (x, y, side, side), self.backgr_imgs[i + 4 * j]
        return None

    def on_click(self, btn):
        if btn:
            if btn[1] == 'done':
                return True
            else:
                self.chosen_backgr = btn
        return False


class FontChoice(Choice):
    def __init__(self, username):
        super().__init__()
        cn = sqlite3.connect(DB)
        self.fonts = list(cn.cursor().execute(f"SELECT Mistral, Chiller, Jokerman, Harrington "
                                              f"FROM results WHERE name='{username}'").fetchall()[0])
        self.fonts.insert(0, 1)
        self.fonts_names = ['Ink Free', 'Mistral', 'Jokerman', 'Chiller', 'Harrington']
        cn.close()
        self.chosen_font = None

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        if not self.btns:
            self.create_fontbtns()
        for btn in self.btns:
            fnt, fnt_size, clr = ('Segoe Script', WIDTH // 17, 100) if not btn[2] else (btn[1], WIDTH // 11, 255)
            text = game_font(fnt_size, fnt).render(btn[1], True, (clr, clr, clr))
            screen.blit(text, (btn[0][0] + 10, btn[0][1]))
            pygame.draw.rect(screen, (clr, clr, clr), (btn[0][0], btn[0][1], btn[0][2], btn[0][3]), 2)
        if self.chosen_font:
            pygame.draw.rect(screen, (76, 187, 23), self.chosen_font[0], 4)

    def create_fontbtns(self):
        for i in range(5):
            if self.fonts[i]:
                is_bought = True
                fnt = txt = self.fonts_names[i]
                text = game_font(WIDTH // 11, fnt).render(txt, True, (255, 255, 255))
            else:
                is_bought = False
                txt = 'Здесь будет ваша покупка'
                text = game_font(WIDTH // 17, 'Segoe script').render(txt, True, (255, 255, 255))
            space = 30 if self.fonts_names[i] not in ('Jokerman', 'Harrington') else 20
            x = WIDTH // 2 - text.get_width() // 2
            y = space * (i + 1) + 100 * i
            if self.fonts_names[i] == 'Chiller':
                y -= 25
            width, height = text.get_width() + 20, text.get_height()
            self.btns.append([(x - 10, y, width, height), txt, is_bought])

    def on_click(self, btn):
        if btn:
            if btn[1] == 'done':
                return True
            else:
                self.chosen_font = btn
        return False


class ModeChoice(Choice):
    def __init__(self):
        super().__init__()
        self.chosen_mode = None

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        text = game_font(WIDTH // 15, 'Segoe script').render('Выберите режим игры:', True, (255, 255, 255))
        x, y = SIDE // 2 - text.get_width() // 2, SIDE // 2 - text.get_height() // 2 - 150
        screen.blit(text, (x, y))
        if not self.btns:
            self.create_btns()
        for btn in self.btns:
            text = game_font(WIDTH // 17, 'Segoe script').render(btn[1], True, (255, 255, 255))
            screen.blit(text, (btn[0][0] + 10, btn[0][1]))
            pygame.draw.rect(screen, (255, 255, 255), (btn[0][0], btn[0][1], btn[0][2], btn[0][3]), 2)
        if self.chosen_mode:
            pygame.draw.rect(screen, (76, 187, 23), self.chosen_mode[0], 4)

    def create_btns(self):
        txt1, txt2 = 'Перевод из двоичной сс', 'Перевод в двоичную сс'
        text1 = game_font(WIDTH // 17, 'Segoe script').render(txt1, True, (255, 255, 255))
        text2 = game_font(WIDTH // 17, 'Segoe script').render(txt2, True, (255, 255, 255))
        x = WIDTH // 2 - text1.get_width() // 2
        y = SIDE // 2
        self.btns = [[(x, y - 70, text1.get_width() + 20, text1.get_height()), txt1, True],
                     [(x, y + 50, text2.get_width() + 20, text1.get_height()), txt2, True]]

    def on_click(self, btn):
        if btn:
            if btn[1] == 'done':
                return True
            else:
                self.chosen_mode = btn
        return False


class DifficultyChoice(Choice):
    def __init__(self):
        super().__init__()
        self.chosen_difficulty = None

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        text = game_font(WIDTH // 14, 'Segoe script').render('Выберите сложность:', True, (255, 255, 255))
        x, y = SIDE // 2 - text.get_width() // 2, SIDE // 2 - text.get_height() // 2 - 200
        screen.blit(text, (x, y))
        if not self.btns:
            self.create_btns()
        for btn in self.btns:
            text = game_font(WIDTH // 21, 'Segoe script').render(btn[1], True, (255, 255, 255))
            screen.blit(text, (btn[0][0] + 10, btn[0][1]))
            pygame.draw.rect(screen, (255, 255, 255), (btn[0][0], btn[0][1], btn[0][2], btn[0][3]), 2)
        if self.chosen_difficulty:
            pygame.draw.rect(screen, (76, 187, 23), self.chosen_difficulty[0], 4)

    def create_btns(self):
        txt1, txt2, txt3 = 'Легко (четверичная сс)', 'Средне (восьмеричная сс)', 'Сложно (шестнадцатиричная сс)'
        text1 = game_font(WIDTH // 21, 'Segoe script').render(txt1, True, (255, 255, 255))
        text2 = game_font(WIDTH // 21, 'Segoe script').render(txt2, True, (255, 255, 255))
        text3 = game_font(WIDTH // 21, 'Segoe script').render(txt3, True, (255, 255, 255))
        x = WIDTH // 2 - text2.get_width() // 2
        y = HEIGHT // 2 - 50
        x3 = WIDTH // 2 - text3.get_width() // 2 - 10
        self.btns = [[(x, y - 70, text1.get_width() + 20, text1.get_height()), txt1, True],
                     [(x, y + 50, text2.get_width() + 20, text1.get_height()), txt2, True],
                     [(x3, y + 170, text3.get_width() + 20, text1.get_height()), txt3, True]]

    def on_click(self, btn):
        if btn:
            if btn[1] == 'done':
                return True
            else:
                self.chosen_difficulty = btn
        return False


def personalization(username):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Подготовка к игре")
    fonts = modes = difficulties = None
    backgrounds = BackgroundChoice(username)
    chosen_btn = None
    font = background = mode = None
    while True:
        screen.fill((34, 2, 74))
        current_class = list(filter(lambda x: x, [fonts, backgrounds, modes, difficulties]))[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = current_class.get_click(event.pos)
                if done:
                    if backgrounds and backgrounds.chosen_backgr:
                        background = backgrounds.chosen_backgr[1]
                        backgrounds = chosen_btn = None
                        fonts = FontChoice(username)
                    elif fonts and fonts.chosen_font:
                        font = fonts.chosen_font[1]
                        fonts = chosen_btn = None
                        modes = ModeChoice()
                    elif modes and modes.chosen_mode:
                        mode = modes.chosen_mode[1]
                        modes = chosen_btn = None
                        difficulties = DifficultyChoice()
                    elif difficulties and difficulties.chosen_difficulty:
                        difficulty = difficulties.chosen_difficulty[1]
                        return font, background, mode, difficulty
            if event.type == pygame.MOUSEMOTION:
                if current_class.donebtn_info:
                    chosen_btn = current_class.get_btn(event.pos)
        current_class.render(screen)
        if chosen_btn:
            pygame.draw.rect(screen, 'purple', chosen_btn[0], 2)
        pygame.display.flip()
