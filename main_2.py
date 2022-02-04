import constants
import pygame
from menu_2 import IntroductionView, Settings, Authorization, Results, User, escape
from main_game import play
from store import store


def main():
    user = User()
    view = IntroductionView(user)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                escape()
            if event.type == pygame.MOUSEMOTION:
                if constants.STAGE == 'Меню':
                    view.animate()
                elif constants.STAGE == 'Магазин':
                    sett = Settings(user)
                    sett.animate()
                elif constants.STAGE == 'Войти в аккаунт':
                    auth = Authorization(user)
                    auth.animate()
                elif constants.STAGE == 'Результаты':
                    res = Results(user)
                    res.animate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if constants.STAGE == 'Меню':
                    view.push_btn()
                elif constants.STAGE == 'Магазин':
                    store(user.name)
                    constants.STAGE = 'Меню'
                    view = IntroductionView(user)
                elif constants.STAGE == 'Результаты':
                    res = Results(user)
                    res.push_btn()
                elif constants.STAGE == 'Играть':
                    play(user.name)
                    constants.STAGE = 'Меню'
                    view = IntroductionView(user)
        pygame.display.flip()


if __name__ == '__main__':
    main()
