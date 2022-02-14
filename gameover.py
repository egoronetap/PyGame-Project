# Anfisa
import sqlite3
import pygame
import random
from constants2 import WIDTH, HEIGHT, DB
from my_functions import game_font, terminate, load_image, create_coin_sprite
from game_classes import AnimatedSprite


class GameOverScreen:
    def __init__(self, username, score, coins, font_name):
        self.username = username
        self.score, self.coins = score, coins
        self.font = font_name
        self.texts, self.info = self.create_btns_info(font_name)
        self.is_bestscore, self.bestscore = self.check_bestscore()
        self.sprites = None

    def render(self, surface):
        gameover_text = game_font(WIDTH // 12, self.font).render("GAME OVER", True, (1, 0, 28))
        score_text = game_font(WIDTH // 12, self.font).render(f"your score: {self.score} ({self.coins}    )",
                                                              True, (1, 0, 28))
        if self.is_bestscore:
            bestscore_text = game_font(WIDTH // 12, self.font).render(f"New Best Score!", True, (1, 0, 28))
        else:
            bestscore_text = game_font(WIDTH // 11, self.font).render(f"best score: {self.bestscore}", True, (1, 0, 28))
        bestscore_x = WIDTH // 2 - bestscore_text.get_width() // 2
        gameover_x = WIDTH // 2 - gameover_text.get_width() // 2
        score_x = WIDTH // 2 - score_text.get_width() // 2
        y = HEIGHT // 4 - gameover_text.get_height() // 2
        if not self.sprites:
            self.sprites = pygame.sprite.Group()
            create_coin_sprite(score_x + score_text.get_width() - 82, y + 2, (54, 65), self.sprites)
        pygame.draw.rect(surface, (186, 172, 199), (WIDTH // 2 - (score_text.get_width() + 61) // 2, 61,
                                                    score_text.get_width() + 61, 238))
        pygame.draw.rect(surface, (61, 40, 89), (WIDTH // 2 - (score_text.get_width() + 61) // 2, 61,
                                                 score_text.get_width() + 61, 238), 4)
        surface.blit(bestscore_text, (bestscore_x, y + 80))
        surface.blit(gameover_text, (gameover_x, y - 80))
        surface.blit(score_text, (score_x, y))
        self.draw_buttons(surface)
        self.sprites.draw(surface)

    def create_btns_info(self, font_name):
        replay_txt = game_font(WIDTH // 10, font_name).render('replay', True, (186, 172, 199))
        replay_btn_info = [WIDTH // 2 - replay_txt.get_width() // 2 - 10, HEIGHT // 1.6,  # x, y
                           replay_txt.get_width() + 18, replay_txt.get_height() - 10]  # width, height
        return_txt = game_font(WIDTH // 14, font_name).render('return to menu', True, (186, 172, 199))
        return_btn_info = [WIDTH // 2 - return_txt.get_width() // 2 - 10, HEIGHT // 1.27,  # x, y
                           return_txt.get_width() + 18, return_txt.get_height() - 10]  # width, height
        return [replay_txt, return_txt], [replay_btn_info, return_btn_info]

    def check_bestscore(self):
        cn = sqlite3.connect(DB)
        cur = cn.cursor()
        bestscore = cur.execute(f"SELECT best_score from results WHERE name='{self.username}'").fetchone()[0]
        if self.score > bestscore:
            cur.execute(f"UPDATE results SET best_score={self.score} WHERE name='{self.username}'")
            cn.commit()
            cn.close()
            return True, bestscore
        return False, bestscore

    def draw_buttons(self, surface):
        for i in range(2):
            info = self.info[i]
            pygame.draw.rect(surface, (1, 0, 28), (info[0], info[1], info[2], info[3]))
            pygame.draw.rect(surface, (255, 255, 255), (info[0], info[1], info[2], info[3]), 2)
            surface.blit(self.texts[i], (info[0] + 10, info[1] - 8))

    def get_btn(self, mouse_pos):
        if self.info[0][0] <= mouse_pos[0] <= self.info[0][0] + self.info[0][2] and \
                self.info[0][1] <= mouse_pos[1] <= self.info[0][1] + self.info[0][3]:
            return 'replay'
        elif self.info[1][0] <= mouse_pos[0] <= self.info[1][0] + self.info[1][2] and \
                self.info[1][1] <= mouse_pos[1] <= self.info[1][1] + self.info[1][3]:
            return 'return to menu'
        return None


def gameover(username, surface, fon_img, score, coins, font_name):
    pygame.display.set_caption('Ничто не вечно')
    gameover_screen = GameOverScreen(username, score, coins, font_name)
    character_sprites = pygame.sprite.Group()
    img = random.choice(['happy1.png', 'happy2.png', 'happy3.png', 'happy4.png']) if score else 'calm_character.png'
    character = AnimatedSprite(character_sprites, load_image(img, -1), 8, 1, WIDTH // 2 - 55, HEIGHT // 2.3)
    character_clock = pygame.time.Clock()
    btn_is_chosen = info = False
    while True:
        fon = pygame.transform.scale(load_image(fon_img), (WIDTH, HEIGHT))
        surface.blit(fon, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN:
                btn = gameover_screen.get_btn(event.pos)
                if btn == 'replay':
                    return True
                elif btn == 'return to menu':
                    return False
            if event.type == pygame.MOUSEMOTION:
                btn = gameover_screen.get_btn(event.pos)
                if btn:
                    btn_is_chosen = True
                    info = gameover_screen.info[0] if btn == 'replay' else gameover_screen.info[1]
                else:
                    btn_is_chosen = False
        gameover_screen.render(surface)
        character_sprites.draw(surface)
        if btn_is_chosen:
            pygame.draw.rect(surface, (32, 15, 128), (info[0], info[1], info[2], info[3]), 2)
        if character_clock.tick(7):
            character.update()
        pygame.display.flip()
