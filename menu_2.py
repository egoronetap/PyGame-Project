import pygame

from constants import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class IntroductionView:
    def __init__(self):
        screen.fill((0, 0, 0))
        self.start()

    def draw(self, x, y, message, color=(255, 255, 255), font_size=30):
        font = pygame.font.Font(None, font_size)
        text = font.render(message, True, color)
        screen.blit(text, (x, y))
        pygame.draw.rect(screen, color, (x - 10, y - 10, text.get_width() + 20, text.get_height() + 20), 1)
        LST_OF_POS.append([x - 10, y - 10, text.get_width() + 20 + x, text.get_height() + 20 + y, message])

    def start(self):
        self.draw(SCREEN_WIDTH // 24, SCREEN_HEIGHT // 18, 'Название игры', (0, 255, 255), font_size=90)
        self.draw(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4, 'Играть', (255, 255, 255), font_size=60)
        self.draw(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + SCREEN_HEIGHT // 8,
                  'Настройки', (255, 255, 255), font_size=60)
        self.draw(SCREEN_WIDTH // 3 + 5, SCREEN_HEIGHT // 4 * 2, 'Выйти', (255, 255, 255), font_size=60)
        self.draw(SCREEN_WIDTH - (SCREEN_WIDTH // 4), SCREEN_HEIGHT - (SCREEN_HEIGHT // 16),
                  'Войти в аккаунт', (255, 255, 255), font_size=20)
        LST_OF_POS.pop(0)

    def animate(self):
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in LST_OF_POS:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    pygame.draw.rect(screen, (255, 0, 0), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)
                else:
                    pygame.draw.rect(screen, (255, 255, 255), (i[0], i[1], i[2] - i[0] - 10, i[3] - i[1] - 10), 1)

    def push_btn(self):
        click = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()

        if 0 < mouse[0] < SCREEN_WIDTH - 1 and 0 < mouse[1] < SCREEN_HEIGHT - 1:
            for i in LST_OF_POS:
                if i[0] <= mouse[0] <= i[2] - 10 and i[1] <= mouse[1] <= i[3] - 10:
                    if i[4] == 'Выйти':
                        escape()
                    elif i[4] == 'Настройки':
                        FLAG = False
                        a = Settings()


class Settings:
    def __init__(self):
        screen.fill((0, 0, 0))


def escape():
    exit()
