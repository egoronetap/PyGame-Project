import pygame
import random
import sqlite3
from constants2 import WIDTH, HEIGHT, DB
from my_functions import game_font, decimal_conversion, load_image, create_coin_sprite


class Buttons:
    def __init__(self, to_sys, font_name):
        self.to_sys = to_sys
        self.font = font_name
        btns_dict = {16: 2, 8: 3, 4: 4, 2: 8}
        self.is_pause = False
        self.btns_n = btns_dict[to_sys]
        self.btn_font = game_font(WIDTH // 12, font_name)
        self.btn_size, self.extrabtn_size = WIDTH // 10, WIDTH // (10 + to_sys // 2)
        self.btns_x = []
        self.btn_y = HEIGHT - self.btn_size - 10  # для всех кнопок одинаковое значение
        self.solution = ['0'] * self.btns_n
        self.extra_btns = [False, None]  # если True, второй элемент - номер кнопки
        self.alphabet = '0123456789ABCDEF'

    def render(self, surface):
        pygame.draw.rect(surface, (186, 172, 199), (WIDTH - 52, 8, 44, 44))  # кнопка паузы
        if not self.is_pause:
            pygame.draw.line(surface, (106, 92, 119), (WIDTH - 36, 16), (WIDTH - 36, 42), 4)
            pygame.draw.line(surface, (106, 92, 119), (WIDTH - 26, 16), (WIDTH - 26, 42), 4)
        else:
            pygame.draw.polygon(surface, (106, 92, 119),
                                ((WIDTH - 39, 16), (WIDTH - 20, 29), (WIDTH - 39, 42)))
        if self.btns_x:
            for i in range(len(self.btns_x)):
                pygame.draw.rect(surface, (186, 172, 199), (self.btns_x[i], self.btn_y, self.btn_size, self.btn_size))
                numb = self.btn_font.render(self.solution[i], True, (61, 40, 89))
                x = self.btns_x[i] + self.btn_size // 2 - numb.get_width() // 2
                y = self.btn_y + self.btn_size // 2 - numb.get_height() // 2
                surface.blit(numb, (x, y))
                if self.extra_btns[0] and self.extra_btns[1] == i and not self.is_pause:
                    self.add_btns(surface, i)
        else:
            for i in range(self.btns_n):
                btn_x = ((WIDTH - self.btn_size * self.btns_n) / (self.btns_n + 1)) * (i + 1) + self.btn_size * i
                self.btns_x.append(btn_x)

    def add_btns(self, surface, i):
        pygame.draw.rect(surface, (186, 172, 199), (self.btns_x[i], self.btn_y - self.extrabtn_size * self.to_sys,
                                                    self.extrabtn_size, self.extrabtn_size * self.to_sys))
        for j in range(self.to_sys):
            x1, y1 = self.btns_x[i], self.btn_y - self.extrabtn_size * (self.to_sys - j - 1)
            x2, y2 = self.btns_x[i] + self.extrabtn_size, self.btn_y - self.extrabtn_size * (self.to_sys - j - 1)
            pygame.draw.line(surface, (106, 92, 119), (x1, y1), (x2, y2), 3)
            new_numb = game_font(WIDTH // (12 + self.to_sys // 2), self.font).render(self.alphabet[j], True,
                                                                                     (61, 40, 89))
            new_x = self.btns_x[i] + self.extrabtn_size // 2 - new_numb.get_width() // 2
            new_y = (self.btn_y + self.extrabtn_size // 2 - new_numb.get_height() // 2) - self.extrabtn_size * (j + 1)
            surface.blit(new_numb, (new_x, new_y))

    def get_btn(self, mouse_pos):  # если кликнули на кнопку, возвращает её номер, иначе None
        if WIDTH - 52 <= mouse_pos[0] <= WIDTH - 8 and 8 <= mouse_pos[1] <= 52:
            return 'pause'
        for i in range(len(self.btns_x)):
            if self.btns_x[i] <= mouse_pos[0] <= self.btns_x[i] + self.btn_size:
                if self.btn_y <= mouse_pos[1] <= self.btn_y + self.btn_size:
                    return [i, 0]
                if self.extra_btns[0]:
                    for j in range(self.to_sys + 1):
                        bottom_line = self.btn_y - self.extrabtn_size * (j - 1)
                        if self.btn_y - self.extrabtn_size * j <= mouse_pos[1] <= bottom_line:
                            return [i, j]  # [номер по горизонтали, номер по вертикали (снизу)]
        return None

    def get_click(self, mouse_pos):
        btn = self.get_btn(mouse_pos)
        if btn == 'pause':
            self.is_pause = not self.is_pause
        elif btn and not self.is_pause:
            self.on_click(btn)

    def on_click(self, btn_xy):
        if not btn_xy[1]:
            if self.to_sys == 2:
                self.solution[btn_xy[0]] = '0' if int(self.solution[btn_xy[0]]) else '1'
            else:
                self.extra_btns = [True, btn_xy[0]] if self.extra_btns[1] != btn_xy[0] else [False, None]
        else:
            self.solution[btn_xy[0]] = self.alphabet[btn_xy[1] - 1]
            self.extra_btns = [False, None]

    def check_solution(self, to_system_numbs):  # постоянная проверка, не набрали ли правильное число
        if any(map(lambda el: el != '0', self.solution)):
            str_solution = ''.join(self.solution)
            while str_solution[0] == '0':
                str_solution = str_solution[1:]
            if str_solution in to_system_numbs:
                return to_system_numbs.index(str_solution)
        return None


class MovingObjectsAndCoins:
    def __init__(self, username, from_sys, to_sys, font_name):
        self.from_sys, self.to_sys = from_sys, to_sys
        self.username = username
        self.cn = sqlite3.connect(DB)
        self.balance = self.cn.cursor().execute(f"SELECT balance FROM results WHERE name='{username}'").fetchone()[0]
        self.coin_n = 5 if 4 in (from_sys, to_sys) else 4 if 8 in (from_sys, to_sys) else 3
        self.font = font_name
        self.numb_list, self.fireworks = [], []
        self.coin_count = self.score = self.coins = 0
        self.character = None
        self.firework_sprites, self.character_sprites = pygame.sprite.Group(), pygame.sprite.Group()
        self.star_sprites, self.coin_sprite_group = pygame.sprite.Group(), pygame.sprite.Group()
        self.star_image = load_image("drawing.png", -1)
        create_coin_sprite(10, 10, (34, 38), self.coin_sprite_group)

    def add_numb(self):
        n = random.randint(1, 255)
        while decimal_conversion(n, self.from_sys) in map(lambda lst: lst[1], self.numb_list):
            n = random.randint(1, 255)
        text = game_font(35, self.font).render(decimal_conversion(n, self.from_sys), True, (0, 0, 0))
        star_sprite = pygame.sprite.Sprite()
        star_sprite.image = pygame.transform.scale(self.star_image, (text.get_width() + 110, text.get_height() + 20))
        star_sprite.rect = star_sprite.image.get_rect()
        x_coord = random.randrange(9, WIDTH - text.get_width() - 115, 3)
        star_sprite.rect.x, star_sprite.rect.y = x_coord, 0
        self.star_sprites.add(star_sprite)
        self.numb_list.append([[x_coord, 0], decimal_conversion(n, self.to_sys), star_sprite, text])

    def render(self, surface, is_pause, t, btns_class_obj):
        coins = game_font(40, 'Ink Free').render(str(self.balance), True, (186, 172, 199))
        pygame.draw.rect(surface, (61, 40, 89), (0, 0, coins.get_width() + 63, 60))
        pygame.draw.rect(surface, (186, 172, 199), (0, 0, coins.get_width() + 63, 60), 2)
        surface.blit(coins, (53, 5))
        self.coin_sprite_group.draw(surface)
        if is_pause:
            self.pause(surface)
        else:
            excess_n = btns_class_obj.check_solution([el[1] for el in self.numb_list])   # пора delete n, тк его набрали
            numb_texts = []
            for i in range(len(self.numb_list)):
                self.numb_list[i][0][1] += t
                self.numb_list[i][2].rect.y = self.numb_list[i][0][1]
                x = self.numb_list[i][0][0] + 55
                y = self.numb_list[i][0][1] + 10
                numb_texts.append((self.numb_list[i][3], (x, y)))
            self.star_sprites.draw(surface)
            for text in numb_texts:  # отдельный цикл, чтобы текст размещался поверх картинок (а не наоборот)
                surface.blit(text[0], text[1])
            if excess_n or excess_n == 0:
                self.delete_excess(excess_n, btns_class_obj)

    def delete_excess(self, n, btns_class_obj):
        coords = self.numb_list[n][0]
        firework = AnimatedSprite(self.firework_sprites, load_image("effect_009.png", -1),
                                  5, 8, coords[0] + self.numb_list[n][3].get_width() // 2 - 40, coords[1] - 40)
        self.fireworks.append([firework, 0])
        self.numb_list[n][2].kill()
        del self.numb_list[n]
        self.score += 1
        self.coin_count += 1
        if self.coin_count == self.coin_n:
            self.balance += 1
            self.coin_count = 0
        btns_class_obj.solution = ['0'] * btns_class_obj.btns_n  # обнуление кнопочек

    def pause(self, surface):
        text = game_font(90, self.font).render("PAUSE", True, (61, 40, 89))
        x = WIDTH // 2 - text.get_width() // 2
        y = HEIGHT // 2 - text.get_height() // 2
        pygame.draw.rect(surface, (186, 172, 199), (x - 10, y - 50, text.get_width() + 20, text.get_height() - 7))
        pygame.draw.rect(surface, (61, 40, 89), (x - 10, y - 50, text.get_width() + 20, text.get_height() - 7), 4)
        surface.blit(text, (x, y - 50))
        if not self.character:
            self.character = AnimatedSprite(self.character_sprites,
                                            load_image("dancing.png", -1), 8, 1, WIDTH // 2 - 50, y + 75)

    def animate_fireworks(self, surface, clock):
        first_animation_end = False
        self.firework_sprites.draw(surface)
        if clock.tick(20):
            for firework in self.fireworks:
                if firework[1] < 40:
                    firework[0].update()
                    firework[1] += 1
                else:
                    first_animation_end = True
            if first_animation_end:
                del self.fireworks[0]

    def check_gameover(self):
        for i in range(len(self.numb_list)):
            if self.numb_list[i][0][1] >= HEIGHT - WIDTH // 10 - 76:
                start_balance = self.cn.cursor().execute(f"SELECT balance FROM results "
                                                         f"WHERE name='{self.username}'")
                self.coins = self.balance - start_balance.fetchone()[0]
                self.cn.cursor().execute(f"UPDATE results SET balance={self.balance} WHERE name='{self.username}'")
                self.cn.commit()
                self.cn.close()
                return True
        return False


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sprite_group, sheet, columns, rows, x, y):
        super().__init__(sprite_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
