import pygame

import sqlite3

import constants
from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# sound1 = pygame.mixer.Sound('Sounds/Blip_Select.wav')
# pygame.mixer.music.load('Sounds/Boulevard Depo - X2.mp3')
# pygame.mixer.music.play()


class IntroductionView:
    def __init__(self):
        self.list_of_pos = list()
        screen.fill((34, 2, 74))
        self.start()

    def draw(self, x, y, message, color=(255, 255, 255), font_size=30, rect=False):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, color)
        screen.blit(text, (x, y))
        if rect:
            pygame.draw.rect(screen, color, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
            self.list_of_pos.append([x - 10, y - 10, text.get_width() + 20 + x, text.get_height() + 20 + y, message])

    def start(self):
        self.draw(SCREEN_WIDTH // 16, SCREEN_HEIGHT // 18, 'Название игры', (0, 255, 255), font_size=120, rect=True)
        self.draw(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4, 'Играть', (255, 255, 255), font_size=90, rect=True)
        self.draw(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + SCREEN_HEIGHT // 7,
                  'Настройки', (255, 255, 255), font_size=90, rect=True)
        self.draw(SCREEN_WIDTH // 4 - 10, SCREEN_HEIGHT // 3 + 145,
                  'Результаты', (255, 255, 255), font_size=90, rect=True)
        self.draw(SCREEN_WIDTH // 3 + 5, SCREEN_HEIGHT // 14 * 10 - 20, 'Выйти',
                  (255, 255, 255), font_size=90, rect=True)
        self.draw(SCREEN_WIDTH - (SCREEN_WIDTH // 3), SCREEN_HEIGHT - (SCREEN_HEIGHT // 14),
                  'Войти в аккаунт', (255, 255, 255), font_size=40, rect=True)
        self.list_of_pos.pop(0)
        if not constants.STATUS:
            self.draw(SCREEN_WIDTH // 20, SCREEN_HEIGHT - (SCREEN_HEIGHT // 14), 'Вы не зарегистрированы',
                      (255, 255, 255), font_size=40)
        else:
            self.draw(10, SCREEN_HEIGHT - 40, constants.NAME,
                      (255, 255, 255), font_size=40)

    def animate(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)

    def push_btn(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    if i[4] == 'Выйти':
                        escape()
                    elif i[4] == 'Настройки':
                        constants.STAGE = 'Настройки'
                        Settings()
                    elif i[4] == 'Войти в аккаунт':
                        constants.STAGE = 'Войти в аккаунт'
                        Authorization()
                    elif i[4] == 'Результаты':
                        constants.STAGE = 'Результаты'
                        Results()


class Settings:
    def __init__(self):
        screen.fill((34, 2, 74))
        self.list_of_pos = list()
        self.option_menu()

    def draw(self, x, y, message, color=(255, 255, 255), font_size=30, rect=False):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, color)
        screen.blit(text, (x, y))
        if rect:
            pygame.draw.rect(screen, color, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
            self.list_of_pos.append([x - 10, y - 10, text.get_width() + 20 + x, text.get_height() + 20 + y, message])

    def option_menu(self):
        self.draw(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 18, 'Настройки', (255, 0, 0), font_size=120, rect=True)
        self.draw(SCREEN_WIDTH // 20, SCREEN_HEIGHT - (SCREEN_HEIGHT // 12), 'Назад',
                  (255, 255, 255), font_size=60, rect=True)
        self.list_of_pos.pop(0)

    def push_btn(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    if i[4] == 'Назад':
                        constants.STAGE = 'Меню'
                        IntroductionView()

    def animate(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)


class Authorization:
    def __init__(self):
        screen.fill((34, 2, 74))
        self.list_of_pos = list()
        self.auth_menu()

    def draw(self, x, y, message, color=(255, 255, 255), font_size=30, rect=False):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, color)
        screen.blit(text, (x, y))
        if rect:
            pygame.draw.rect(screen, color, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
            self.list_of_pos.append([x - 10, y - 10, text.get_width() + 20 + x, text.get_height() + 20 + y, message])

    def auth_menu(self):
        self.draw(SCREEN_WIDTH // 22, SCREEN_HEIGHT // 18, 'Вход в аккаунт', (0, 255, 255), font_size=120, rect=True)
        self.draw(SCREEN_WIDTH // 20, SCREEN_HEIGHT - (SCREEN_HEIGHT // 12),
                  'Назад', (255, 255, 255), font_size=60, rect=True)
        self.draw(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 4, 'Имя пользователя', (255, 255, 255), font_size=60)
        self.draw(SCREEN_WIDTH // 3 + 10, SCREEN_HEIGHT // 2 - 60, 'Пароль', (255, 255, 255), font_size=60)
        self.draw(SCREEN_WIDTH // 3 - 120, SCREEN_HEIGHT // 2 + 80, 'Войти', (255, 255, 255), font_size=80, rect=True)
        self.draw(SCREEN_WIDTH // 3 + 80, SCREEN_HEIGHT // 2 + 80, 'Создать', (255, 255, 255), font_size=80, rect=True)
        self.list_of_pos.pop(0)

        font = pygame.font.Font(None, 60)
        clock = pygame.time.Clock()
        self.input_box = pygame.Rect(100, 220, 460, 60)
        self.input_box1 = pygame.Rect(100, 340, 460, 60)
        color_inactive = pygame.Color((255, 255, 255))
        color_active = pygame.Color((255, 0, 0))
        color = color_inactive
        color1 = color_inactive
        self.active = False
        self.active1 = False
        self.text = ''
        self.text1 = ''
        done = False

        while not done and constants.STAGE == 'Войти в аккаунт':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.MOUSEMOTION and constants.STAGE == 'Войти в аккаунт':
                    self.animate()
                if event.type == pygame.MOUSEBUTTONDOWN and constants.STAGE == 'Войти в аккаунт':
                    self.set_active_for_name()
                    self.set_active_for_password()
                    # Change the current color of the input box.
                    color = color_active if self.active else color_inactive
                    color1 = color_active if self.active1 else color_inactive
                    self.push_btn()
                if event.type == pygame.KEYDOWN and constants.STAGE == 'Войти в аккаунт':
                    if self.active:
                        if event.key == pygame.K_RETURN:
                            print(self.text)
                            self.text = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode
                    if self.active1:
                        if event.key == pygame.K_RETURN:
                            print(self.text1)
                            self.text1 = ''
                        elif event.key == pygame.K_BACKSPACE:
                            self.text1 = self.text1[:-1]
                        else:
                            self.text1 += event.unicode

            # Render the current text.
            if constants.STAGE == 'Войти в аккаунт':
                pygame.draw.rect(screen, (34, 2, 74), (100, 220, 700, 60))
                pygame.draw.rect(screen, (34, 2, 74), (100, 340, 700, 60))
                txt_surface = font.render(self.text, True, color)
                txt_surface1 = font.render(self.text1, True, color1)
                # Resize the box if the text is too long.
                if txt_surface.get_width() >= 450:
                    width = max(200, txt_surface.get_width() + 10)
                    self.input_box.w = width
                else:
                    self.input_box.w = 460
                if txt_surface1.get_width() >= 450:
                    width = max(200, txt_surface1.get_width() + 10)
                    self.input_box1.w = width
                else:
                    self.input_box1.w = 460
                # Blit the text.
                screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
                screen.blit(txt_surface1, (self.input_box1.x + 5, self.input_box1.y + 5))
                # Blit the input_box rect.
                pygame.draw.rect(screen, color, self.input_box, 2)
                pygame.draw.rect(screen, color1, self.input_box1, 2)

                pygame.display.flip()
                clock.tick(30)

    def set_active_for_name(self):
        if self.input_box.collidepoint(pygame.mouse.get_pos()):
            # Toggle the active variable.
            self.active = not self.active
        else:
            self.active = False

    def set_active_for_password(self):
        if self.input_box1.collidepoint(pygame.mouse.get_pos()):
            # Toggle the active variable.
            self.active1 = not self.active
        else:
            self.active1 = False

    def register(self):
        pygame.draw.rect(screen, (34, 2, 74), (190, SCREEN_HEIGHT - 55, 700, 300))
        print(f'Your name is {self.text}')
        print(f'Your password is {self.text1}')

        if self.text1 == '' or self.text == '':
            self.draw(190, SCREEN_HEIGHT - 55, 'Не все поля заполнены', (255, 255, 255), font_size=60)
        else:
            flag = True
            pygame.draw.rect(screen, (34, 2, 74), (190, SCREEN_HEIGHT - 55, 700, 300))
            cn = sqlite3.connect(DB)

            cur = cn.cursor()

            records = cur.execute(f'''SELECT name FROM results''').fetchall()
            for i in records:
                print(self.text == i[0])
                if self.text == i[0]:
                    self.draw(190, SCREEN_HEIGHT - 55, 'Данное имя уже занято', (255, 255, 255), font_size=60)
                    flag = False
            if flag:
                cur.execute(f'''INSERT INTO results('name','password','balance','best_score') 
                VALUES('{self.text}', '{self.text1}', 0, 0)''').fetchall()

                cn.commit()
                cn.close()

                constants.NAME = self.text
                constants.STAGE = 'Меню'
                constants.STATUS = True
                IntroductionView()

    def log_in(self):
        pygame.draw.rect(screen, (34, 2, 74), (190, SCREEN_HEIGHT - 55, 700, 300))
        if self.text1 == '' or self.text == '':
            self.draw(190, SCREEN_HEIGHT - 55, 'Не все поля заполнены', (255, 255, 255), font_size=60)
        else:
            flag = False
            pygame.draw.rect(screen, (34, 2, 74), (190, SCREEN_HEIGHT - 55, 700, 300))
            cn = sqlite3.connect(DB)

            cur = cn.cursor()

            records = cur.execute(f'''SELECT name FROM results WHERE password="{self.text1}"''').fetchall()
            if records:
                cn.close()

                constants.NAME = self.text
                constants.STAGE = 'Меню'
                constants.STATUS = True
                IntroductionView()
            else:
                self.draw(190, SCREEN_HEIGHT - 55, 'Неправильное имя или пароль', (255, 255, 255), font_size=45)

    def animate(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)

    def push_btn(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    if i[4] == 'Назад':
                        constants.STAGE = 'Меню'
                        IntroductionView()
                    if i[4] == 'Войти':
                        self.log_in()
                    elif i[4] == 'Создать':
                        self.register()


class Results:
    def __init__(self):
        screen.fill((34, 2, 74))
        self.list_of_pos = list()
        self.show_results()

    def draw(self, x, y, message, color=(255, 255, 255), font_size=30, rect=False):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, color)
        screen.blit(text, (x, y))
        if rect:
            pygame.draw.rect(screen, color, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
            self.list_of_pos.append([x - 10, y - 10, text.get_width() + 20 + x, text.get_height() + 20 + y, message])

    def show_results(self):
        count = 0
        x_coor = 40
        y_coor = 180
        colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (90, 90, 90), (90, 90, 90)]
        self.draw(SCREEN_WIDTH // 6, SCREEN_HEIGHT // 18, 'Результаты', (0, 255, 255), font_size=120, rect=True)
        self.draw(SCREEN_WIDTH // 20, SCREEN_HEIGHT - (SCREEN_HEIGHT // 12),
                  'Назад', (255, 255, 255), font_size=60, rect=True)
        self.list_of_pos.pop(0)

        cn = sqlite3.connect(DB)

        cur = cn.cursor()

        records = cur.execute(f'''SELECT * FROM results ORDER BY best_score DESC''').fetchall()

        cn.close()

        for user in records:
            if count == 6:
                break
            self.draw(x_coor, y_coor, f'{str(count + 1)}){str(user[1])}:', colors[count], font_size=60)
            x_coor += 400
            self.draw(x_coor, y_coor, str(user[3]), colors[count], font_size=60)
            x_coor -= 400
            y_coor += 80
            count += 1

    def push_btn(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    if i[4] == 'Назад':
                        constants.STAGE = 'Меню'
                        IntroductionView()

    def animate(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in self.list_of_pos:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)


def escape():
    exit()
