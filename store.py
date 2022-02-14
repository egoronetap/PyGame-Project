# Anfisa
import pygame
import sqlite3
from my_functions import load_image, game_font, terminate, create_coin_sprite
from constants2 import *


class StoreScreen:
    def __init__(self, username):
        self.username = username
        self.cn = sqlite3.connect(DB)
        self.product = [0, 'background']
        self.backgrs = list(self.cn.cursor().execute(f"SELECT river, asia, forest, green_street, house, idk, leaves, "
                                                     f"mountain, sky, night_forest, night_water, "
                                                     f"romantic_forest, street, sunset, sunrise FROM results "
                                                     f"WHERE name='{username}'").fetchall()[0])
        self.backgr_imgs = ['river', 'asia', 'forest', 'green_street', 'house', 'idk', 'leaves', 'mountain', 'sky',
                            'night_forest', 'night_water', 'romantic_forest', 'street', 'sunset', 'sunrise']
        self.fonts = list(self.cn.cursor().execute(f"SELECT Mistral, Chiller, Jokerman, Harrington "
                                                   f"FROM results WHERE name='{username}'").fetchall()[0])
        self.fonts_names = ['Mistral', 'Chiller', 'Jokerman', 'Harrington']
        self.coin_img = load_image('lil_coins.png', -1)
        self.sprites = self.current_sprite = None
        self.n_is_changed = self.additional_btns = False
        self.balance = self.cn.cursor().execute(f"SELECT balance FROM results WHERE name='{username}'").fetchone()[0]

    def render(self, screen):
        if not self.sprites:
            self.sprites = pygame.sprite.Group()
            create_coin_sprite(WIDTH - WIDTH * 0.08, HEIGHT * 0.03, (40, 43), self.sprites)
            create_coin_sprite(WIDTH // 2 + WIDTH // 30, HEIGHT * 0.86, (70, 75), self.sprites)
        if self.n_is_changed or not self.current_sprite:
            if self.product[1] == 'background':
                self.create_background_sprite()
            else:
                self.current_sprite.kill()
                text = game_font(140, self.fonts_names[self.product[0]]).render(self.fonts_names[self.product[0]],
                                                                                True, (186, 172, 199))
                x, y = WIDTH // 2 - text.get_width() // 2,  HEIGHT // 2 - text.get_height() // 2
                screen.blit(text, (x, y))
        self.sprites.draw(screen)
        self.draw_btns(screen)
        self.add_text(screen)
        if self.additional_btns:
            pygame.draw.rect(screen, (186, 172, 199), (WIDTH * 0.2, HEIGHT * 0.35, WIDTH * 0.6, HEIGHT * 0.3))
            pygame.draw.rect(screen, (61, 40, 89), (WIDTH * 0.2, HEIGHT * 0.35, WIDTH * 0.6, HEIGHT * 0.3), 3)
            text = game_font(70, 'Mistral').render('Купить?',  True, (61, 40, 89))
            x, y = WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2
            screen.blit(text, (x, y - 20))
            pygame.draw.rect(screen, (61, 40, 89), (WIDTH * 0.3, HEIGHT * 0.55, WIDTH * 0.15, HEIGHT * 0.08), 3)
            pygame.draw.rect(screen, (61, 40, 89), (WIDTH * 0.55, HEIGHT * 0.55, WIDTH * 0.15, HEIGHT * 0.08), 3)
            screen.blit(game_font(35, 'Mistral').render('Ой, нет',  True, (61, 40, 89)), (x - 30, y + HEIGHT * 0.11))
            screen.blit(game_font(35, 'Mistral').render('Да!!',  True, (61, 40, 89)), (x + 170, y + HEIGHT * 0.11))

    def create_background_sprite(self):
        if self.current_sprite:
            self.current_sprite.kill()
        self.current_sprite = pygame.sprite.Sprite()
        img = load_image(f'{self.backgr_imgs[self.product[0]]}.jpg')
        self.current_sprite.image = pygame.transform.scale(img, (SIDE * 0.7, SIDE * 0.7))
        self.current_sprite.rect = self.current_sprite.image.get_rect()
        self.current_sprite.rect.x, self.current_sprite.rect.y = WIDTH * 0.15, HEIGHT * 0.13
        self.sprites.add(self.current_sprite)

    def draw_btns(self, screen):
        pygame.draw.rect(screen, (61, 40, 89), (0, 0, 150, 60))
        pygame.draw.rect(screen, (186, 172, 199), (0, 0, 150, 60), 2)
        pygame.draw.rect(screen, (61, 40, 89), (263, 599, 198, 97), 2)
        if not (self.product[0] == 0 and self.product[1] == 'background'):
            pygame.draw.rect(screen, (186, 172, 199), (20, HEIGHT - 70, 70, 50))
            pygame.draw.polygon(screen, (106, 92, 119), ((50, HEIGHT - 65), (30, HEIGHT - 45), (50, HEIGHT - 25),
                                                         (50, HEIGHT - 35), (80, HEIGHT - 35), (80, HEIGHT - 55),
                                                         (50, HEIGHT - 55)))
        if not (self.product[0] == len(self.fonts_names) - 1 and self.product[1] == 'font'):
            pygame.draw.rect(screen, (186, 172, 199), (WIDTH - 90, HEIGHT - 70, 70, 50))
            pygame.draw.polygon(screen, (106, 92, 119), ((WIDTH - 50, HEIGHT - 65), (WIDTH - 30, HEIGHT - 45),
                                                         (WIDTH - 50, HEIGHT - 25), (WIDTH - 50, HEIGHT - 35),
                                                         (WIDTH - 80, HEIGHT - 35), (WIDTH - 80, HEIGHT - 55),
                                                         (WIDTH - 50, HEIGHT - 55)))

    def add_text(self, screen):
        if self.product[1] == 'background':
            price = 'Куплено' if self.backgrs[self.product[0]] else \
                '60' if self.backgr_imgs[self.product[0]] in ('romantic_forest', 'asia', 'green_street') else \
                    '5' if self.backgr_imgs[self.product[0]] == 'river' else '50'
        else:
            price = 'Куплено' if self.fonts[self.product[0]] else \
                '25' if self.fonts_names[self.product[0]] in ('Jokerman', 'Harrington') else '20'
        text = game_font(50, 'Mistral').render('В меню', True, (186, 172, 199))
        screen.blit(text, (150 // 2 - text.get_width() // 2, 30 - text.get_height() // 2))
        text = game_font(90, 'Mistral').render(price, True, (186, 172, 199))
        if self.product[1] == 'background' and self.backgrs[self.product[0]] or \
                self.product[1] == 'font' and self.fonts[self.product[0]]:
            x = WIDTH // 2 - text.get_width() // 2
            pygame.draw.rect(screen, (61, 40, 89), (x - 10, 599, text.get_width() + 20, 97))
            pygame.draw.rect(screen, (186, 172, 199), (x - 10, 599, text.get_width() + 20, 97), 2)
        else:
            x = WIDTH // 1.9 - text.get_width()
        screen.blit(text, (x, HEIGHT * 0.92 - 50))
        text = game_font(50, 'Ink Free').render(str(self.balance), True, (186, 172, 199))
        x = WIDTH - WIDTH * 0.08 - text.get_width() - 5
        y = HEIGHT * 0.03
        screen.blit(text, (x, y - 10))

    def get_click(self, mouse_pos, screen):
        btn = self.get_btn(mouse_pos)
        if btn == 'exit':
            return True
        elif btn:
            self.on_click(btn, screen)
        return False

    def get_btn(self, mouse_pos):
        if self.additional_btns:
            if HEIGHT * 0.55 <= mouse_pos[1] <= HEIGHT * 0.55 + HEIGHT * 0.08:
                if WIDTH * 0.3 <= mouse_pos[0] <= WIDTH * 0.3 + WIDTH * 0.15:
                    return 'no'
                if WIDTH * 0.55 <= mouse_pos[0] <= WIDTH * 0.55 + WIDTH * 0.15:
                    return 'yes'
        else:
            if self.product[1] == 'background' and not self.backgrs[self.product[0]] or \
                    self.product[1] == 'font' and not self.fonts[self.product[0]]:
                if 263 <= mouse_pos[0] <= 263 + 198 and 599 <= mouse_pos[1] <= 599 + 97:
                    return 'buy'
            if 0 <= mouse_pos[0] <= 150 and 0 <= mouse_pos[1] <= 60:
                return 'exit'
            if HEIGHT - 70 <= mouse_pos[1] <= HEIGHT - 70 + 50:
                if 20 <= mouse_pos[0] <= 20 + 70 and not (self.product[0] == 0 and self.product[1] == 'background'):
                    return 'left'
                if WIDTH - 90 <= mouse_pos[0] <= WIDTH - 90 + 70 and \
                        not (self.product[0] == len(self.fonts_names) - 1 and self.product[1] == 'font'):
                    return 'right'
        return None

    def on_click(self, btn, screen):
        if self.product[1] == 'background':
            n = 60 if self.backgr_imgs[self.product[0]] in ('romantic_forest', 'asia', 'green_street') else \
                5 if self.backgr_imgs[self.product[0]] == 'river' else 50
        else:
            n = 25 if self.fonts_names[self.product[0]] in ('Jokerman', 'Harrington') else 20
        if btn == 'buy':
            if self.balance - n >= 0:
                self.additional_btns = True
            else:
                pygame.draw.rect(screen, 'red', (263, 599, 198, 97))
        elif self.additional_btns:
            if btn == 'yes':
                if self.product[1] == 'background':
                    el = self.backgr_imgs[self.product[0]]
                    self.backgrs[self.product[0]] = 1
                else:
                    el = self.fonts_names[self.product[0]]
                    self.fonts[self.product[0]] = 1
                self.cn.cursor().execute(f"UPDATE results SET {el}=True WHERE name='{self.username}'")
                self.cn.cursor().execute(f"UPDATE results SET balance={self.balance - n} WHERE name='{self.username}'")
                self.cn.commit()
                self.balance -= n
            self.additional_btns = False
        else:
            self.n_changing(btn)

    def n_changing(self, btn):
        self.n_is_changed = True
        if btn == 'left':
            if self.product[0] == 0 and self.product[1] == 'font':
                self.product[0], self.product[1] = len(self.backgr_imgs) - 1, 'background'
            else:
                self.product[0] -= 1
        else:
            if self.product[0] == len(self.backgr_imgs) - 1 and self.product[1] == 'background':
                self.product[0], self.product[1] = 0, 'font'
            else:
                self.product[0] += 1


def store(username):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption('Добро пожаловать в магазинчик!)')
    store_screen = StoreScreen(username)
    chosen_btn = None
    while True:
        fon = pygame.transform.scale(load_image('space.jpg'), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                store_screen.cn.close()
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                return_to_menu = store_screen.get_click(event.pos, screen)
                if return_to_menu:
                    store_screen.cn.close()
                    return
            if event.type == pygame.MOUSEMOTION:
                chosen_btn = store_screen.get_btn(event.pos)
        store_screen.render(screen)
        if chosen_btn == 'buy':
            pygame.draw.rect(screen, (201, 180, 255), (263, 599, 198, 97), 2)
        elif chosen_btn == 'exit':
            pygame.draw.rect(screen, (61, 40, 129), (0, 0, 150, 60), 2)
        pygame.display.flip()
