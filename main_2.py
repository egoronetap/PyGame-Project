import constants
import pygame
from menu_2 import IntroductionView, Settings, Authorization, Results


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
                elif constants.STAGE == 'Настройки':
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
                elif constants.STAGE == 'Настройки':
                    sett = Settings()
                    sett.push_btn()
                elif constants.STAGE == 'Результаты':
                    res = Results()
                    res.push_btn()
        pygame.display.flip()


if __name__ == '__main__':
    main()
