from constants import *
import pygame
from menu_2 import IntroductionView


def main():
    view = IntroductionView()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION and FLAG:
                view.animate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                view.push_btn()
        pygame.display.flip()


if __name__ == '__main__':
    main()
