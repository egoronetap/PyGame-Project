# Anfisa
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


def create_coin_sprite(x, y, img_size, sprites):
    coin_img = load_image('lil_coins.png', -1)
    coin_sprite = pygame.sprite.Sprite()
    coin_sprite.image = pygame.transform.scale(coin_img, img_size)
    coin_sprite.rect = coin_sprite.image.get_rect()
    coin_sprite.rect.x, coin_sprite.rect.y = x, y
    sprites.add(coin_sprite)


def terminate():
    pygame.quit()
    sys.exit()
