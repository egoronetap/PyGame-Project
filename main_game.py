import pygame
from constants2 import SIZE, WIDTH, HEIGHT
from my_functions import terminate, load_image
from game_classes import Buttons, MovingObjectsAndCoins
from gameover import gameover

pygame.init()


def play(username, from_sys=16, to_sys=2, fon_img='space.jpg', font_name='Ink Free'):
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Let's gooooo")
    if to_sys == 2:
        frequency = 4500
        speed = 35
    else:
        frequency = 7000
        speed = 25
    MYEVENTTYPE = pygame.USEREVENT + 1  # каждые frequency миллисекунд падает новое число
    pygame.time.set_timer(MYEVENTTYPE, frequency)
    clock, firework_clock, character_clock = pygame.time.Clock(), pygame.time.Clock(), pygame.time.Clock()
    game_is_over = False
    btns = Buttons(to_sys, font_name)
    moving_objs = MovingObjectsAndCoins(username, from_sys, to_sys, font_name)
    while True:
        fon = pygame.transform.scale(load_image(fon_img), (WIDTH, HEIGHT))
        screen.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                moving_objs.cn.close()
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                btns.get_click(event.pos)
            if event.type == MYEVENTTYPE and not (game_is_over + btns.is_pause):
                moving_objs.add_numb()
        if btns.is_pause:
            clock.tick()
            moving_objs.render(screen, True, 0, btns)
            btns.render(screen)
            moving_objs.character_sprites.draw(screen)
            if character_clock.tick(10):
                moving_objs.character.update()
        elif not game_is_over:
            t = speed * clock.tick() / 1000
            moving_objs.render(screen, False, t, btns)
            btns.render(screen)
            if moving_objs.fireworks:
                moving_objs.animate_fireworks(screen, firework_clock)
            game_is_over = moving_objs.check_gameover()
        else:  # game is over
            replay = gameover(username, screen, fon_img, moving_objs.score, moving_objs.coins, font_name)
            if replay:
                game_is_over = False
                pygame.display.set_caption("Let's gooooo")
                btns = Buttons(to_sys, font_name)
                moving_objs = MovingObjectsAndCoins(username, from_sys, to_sys, font_name)
                clock.tick()
            else:
                return
        pygame.display.flip()


if __name__ == '__main__':
    play('user3')
