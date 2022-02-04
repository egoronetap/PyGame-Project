import sqlite3

import pygame
from constants2 import *
from my_functions import load_image, terminate, game_font

pygame.init()


def create_done_btn(screen):
    text = game_font(WIDTH // 14, 'Mistral').render("Готово", True, (255, 255, 255))
    x, y = SIDE - text.get_width() - 50, 635
    width, height = text.get_width() + 24, text.get_height() + 10
    return [text, x, y, width, height]


class BackgroundChoice:
    def __init__(self, username):
        cn = sqlite3.connect(DB)
        self.backgrs = list(cn.cursor().execute(f"SELECT asia, forest, green_street, house, idk, leaves, "
                                                f"mountain, sky, night_forest, night_water, river, "
                                                f"romantic_forest, street, sunset, sunrise FROM results "
                                                f"WHERE name='{username}'").fetchall()[0])
        self.backgrs = [True, True, False, True, False, True, False, True, True, False, True, True, True, False, True]
        self.backgrs.insert(0, 1)
        self.backgr_imgs = ['space', 'asia', 'forest', 'green_street', 'house', 'idk', 'leaves', 'mountain', 'sky',
                            'night_forest', 'night_water', 'river', 'romantic_forest', 'street', 'sunset', 'sunrise']
        cn.close()
        self.sprites = self.donebtn_info = self.chosen_backgr = None

    def render(self, screen):
        if not self.sprites:
            self.create_sprites()
        self.sprites.draw(screen)
        if not self.donebtn_info:
            self.donebtn_info = create_done_btn(screen)
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        if self.chosen_backgr:
            pygame.draw.rect(screen, (76, 187, 23), self.chosen_backgr[0], 5)

    def create_sprites(self):
        self.sprites = pygame.sprite.Group()
        side, space = SIDE * 0.187, SIDE * 0.028
        for i in range(4):
            for j in range(4):
                if self.backgrs[i + 4 * j]:
                    sprite = pygame.sprite.Sprite()
                    img = load_image(f'{self.backgr_imgs[i + 4 * j]}.jpg')
                    sprite.image = pygame.transform.scale(img, (side, side))
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = SIDE * 0.06 + space * (i + 1) + side * i
                    sprite.rect.y = space * (j + 1) + side * j
                    self.sprites.add(sprite)
                else:
                    # ¯\_(ツ)_/¯
                    pass
        return

    def get_click(self, mouse_pos):
        btn = self.get_btn(mouse_pos)
        done = self.on_click(btn)
        return done

    def get_btn(self, mouse_pos):
        text, x, y, width, height = list(self.donebtn_info)
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            return (x, y, width, height), 'done'
        side, space = SIDE * 0.187, SIDE * 0.028
        for i in range(4):
            x = SIDE * 0.06 + space * (i + 1) + side * i
            for j in range(4):
                y = space * (j + 1) + side * j
                if x <= mouse_pos[0] <= x + side and y <= mouse_pos[1] <= y + side and self.backgrs[i + 4 * j]:
                    return (x, y, side, side), self.backgr_imgs[i + 4 * j]
        return None

    def on_click(self, btn):
        if btn[1] == 'done':
            return True
        elif btn:
            self.chosen_backgr = btn
        return False


class FontChoice:
    def __init__(self, username):
        cn = sqlite3.connect(DB)
        self.fonts = list(cn.cursor().execute(f"SELECT Mistral, Chiller, Jokerman, Harrington "
                                              f"FROM results WHERE name='{username}'").fetchall()[0])
        self.fonts.insert(0, 1)
        self.fonts_names = ['Ink Free', 'Mistral', 'Chiller', 'Jokerman', 'Harrington']
        cn.close()
        self.donebtn_info = None
        self.font_btns = []

    def render(self, screen):
        if not self.donebtn_info:
            self.donebtn_info = create_done_btn(screen)
        pygame.draw.rect(screen, (255, 255, 255), (self.donebtn_info[1], self.donebtn_info[2],
                                                   self.donebtn_info[3], self.donebtn_info[4]), 1)
        screen.blit(self.donebtn_info[0], (self.donebtn_info[1] + 12, self.donebtn_info[2]))
        if not self.font_btns:
            self.create_fontbtns()
        for btn in self.font_btns:


    def create_fontbtns(self):
        for i in range(4):
            space = 30
            text = game_font(WIDTH // 8, self.fonts_names[i]).render(self.fonts_names[i], True, (255, 255, 255))
            x = WIDTH // 2 - text.get_width() // 2
            y = space * (i + 1) + 100 * i
            self.font_btns.append([x, y, ])

    def get_click(self, mouse_pos):
        btn = self.get_btn(mouse_pos)
        done = self.on_click(btn)
        return done

    def get_btn(self, mouse_pos):
        text, x, y, width, height = list(self.donebtn_info)
        if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
            return (x, y, width, height), 'done'
        for i in range(4):
            if x <= mouse_pos[0] <= x + side and y <= mouse_pos[1] <= y + side and self.backgrs[i + 4 * j]:
                return (x, y, side, side), self.fonts_names[i + 4 * j]
        return None

    def on_click(self, btn):
        if btn[1] == 'done':
            return True
        elif btn:
            self.chosen_backgr = btn
        return False


def personalization(username):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Подготовка к игре")
    fonts = None
    backgrounds = BackgroundChoice(username)
    choice3 = choice4 = None
    chosen_btn = None
    font = background = c3 = c4 = None
    while True:
        screen.fill((34, 2, 74))
        current_class = list(filter(lambda x: x, [fonts, backgrounds, choice3, choice4]))[0]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if backgrounds:
                    done = backgrounds.get_click(event.pos)
                    if done:
                        if backgrounds.chosen_backgr:
                            background = backgrounds.chosen_backgr
                            backgrounds = chosen_btn = None
                            fonts = FontChoice(username)
            if event.type == pygame.MOUSEMOTION:
                if backgrounds:
                    if backgrounds.donebtn_info:
                        chosen_btn = backgrounds.get_btn(event.pos)
        current_class.render(screen)
        if chosen_btn:
            pygame.draw.rect(screen, 'purple', chosen_btn[0], 2)
        pygame.display.flip()


if __name__ == '__main__':
    personalization('user3')
