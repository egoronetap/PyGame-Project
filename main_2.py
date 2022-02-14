# Egor + Anfisa (только что касается кнопки "Играть")
import constants
import pygame
from menu_2 import IntroductionView, Settings, Authorization, Results, User, escape
from main_game import play
from store import store
from personalization import personalization


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
                    font, backgr, mode, difficulty = personalization(user.name)
                    if 'из' in mode:
                        from_sys = 2
                        to_sys = 16 if 'шест' in difficulty else 8 if 'вос' in difficulty else 4
                    else:
                        to_sys = 2
                        from_sys = 16 if 'шест' in difficulty else 8 if 'вос' in difficulty else 4
                    play(user.name, font_name=font, fon_img=f'{backgr}.jpg', to_sys=to_sys, from_sys=from_sys)
                    constants.STAGE = 'Меню'
                    view = IntroductionView(user)
        pygame.display.flip()


if __name__ == '__main__':
    main()
