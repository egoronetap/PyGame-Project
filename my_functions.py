import pygame
import os
import sys


def game_font(font_size, font_name):
    return pygame.font.SysFont(font_name, font_size)


def decimal_conversion(n, res_system):  # десятичное число(int) и сс, в которую надо перевести(int)
    result = []
    alphabet = '0123456789ABCDEF'
    while n >= res_system:
        new_n = n // res_system
        result.append(alphabet[n - (new_n * res_system)])
        n = new_n
    if n > 0:
        result.append(alphabet[n])
    return ''.join(result)[::-1]


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if color_key:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def terminate():
    pygame.quit()
    sys.exit()
