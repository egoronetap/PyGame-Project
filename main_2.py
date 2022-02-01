import constants
import pygame
from menu_2 import IntroductionView, Settings, Authorization, Results
from main_game import game
from store import store


def main():
    view = IntroductionView()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if constants.STAGE == 'Меню':
                    view.animate()
                elif constants.STAGE == 'Магазин':
                    sett = Settings()
                    sett.animate()
                elif constants.STAGE == 'Войти в аккаунт':
                    auth = Authorization()
                    auth.animate()
                elif constants.STAGE == 'Результаты':
                    res = Results()
                    res.animate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if constants.STAGE == 'Меню':
                    view.push_btn()
                elif constants.STAGE == 'Магазин':
                    store()
                    constants.STAGE = 'Меню'
                    view = IntroductionView()
                elif constants.STAGE == 'Результаты':
                    res = Results()
                    res.push_btn()
                elif constants.STAGE == 'Играть':
                    game()
                    constants.STAGE = 'Меню'
                    view = IntroductionView()
        pygame.display.flip()


if __name__ == '__main__':
    main()
