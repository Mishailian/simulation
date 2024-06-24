import pygame
import sys
import json
from OpenGL.GL import *
from OpenGL.GLUT import *
from game import Game
from static import Static

class GameMenu:
    def __init__(self):
        # Инициализация Pygame
        self.static = Static()
        pygame.init()

        # Размеры окна
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Заголовок окна
        pygame.display.set_caption("Меню игры")

        # Цвета
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.grey = (100, 100, 100)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)
        self.blue = (0, 0, 200)
        self.dark_blue = (0, 0, 100)
        self.dark_red = (100, 0, 0)
        self.dark_green = (0, 100, 0)

        # Шрифты
        self.font = pygame.font.SysFont("Arial", 50)
        self.small_font = pygame.font.SysFont("Arial", 30)

        # Глобальные переменные для юнитов и результатов
        self.number_of_units = 10
        self.results_file = "results.json"
        self.config_file = "config.json"

        # Загрузка фоновых изображений
        self.background_image_main = pygame.image.load("./background_image_main.png")
        self.background_image_main = pygame.transform.scale(self.background_image_main, (self.screen_width, self.screen_height))

        self.background_image_results = pygame.image.load("./background_image_results.png")
        self.background_image_results = pygame.transform.scale(self.background_image_results, (self.screen_width, self.screen_height))

        self.background_image_units = pygame.image.load("./background_image_units.png")
        self.background_image_units = pygame.transform.scale(self.background_image_units, (self.screen_width, self.screen_height))

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)

    def create_button(self, text, x, y, width, height, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            pygame.draw.rect(self.screen, active_color, (x, y, width, height))
            if click[0] == 1 and action is not None:
                action()
                pygame.time.wait(200)  # Задержка для одного клика
        else:
            pygame.draw.rect(self.screen, inactive_color, (x, y, width, height))

        self.draw_text(text, self.small_font, self.white, self.screen, x + (width / 2), y + (height / 2))

    def start_game(self):
        config_data = {"number_of_units": self.number_of_units}
        with open('config.json', "w") as config_file:
            json.dump(config_data, config_file)
        game = Game()
        game.state.create_hero()
        for i in range(0, game.count_of_objects):
            game.state.create_new_object()
        game.main()

    def select_units_menu(self):
        selecting = True
        while selecting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background_image_units, (0, 0))
            self.create_button("Выйти в главное меню", self.screen_width / 2 - 150, 50, 300, 50, self.dark_red, self.red, self.game_menu)
            self.draw_text("Выберите количество юнитов", self.font, self.white, self.screen, self.screen_width / 2, self.screen_height / 4)
            self.draw_text(f"{self.number_of_units}", self.font, self.white, self.screen, self.screen_width / 2, self.screen_height / 2)

            self.create_button("-", self.screen_width / 2 - 150, self.screen_height / 2 - 25, 50, 50, self.dark_red, self.red, self.static.decrease_units())
            self.create_button("+", self.screen_width / 2 + 100, self.screen_height / 2 - 25, 50, 50, self.dark_green, self.green, self.static.increase_units())
            self.create_button("Начать", self.screen_width / 2 - 100, self.screen_height / 1.2, 200, 50, self.dark_blue, self.blue, self.start_game)

            pygame.display.update()

    def show_results(self):
        showing = True
        while showing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        showing = False

            self.screen.blit(self.background_image_results, (0, 0))
            self.draw_text("Топ 10 результатов", self.font, self.white, self.screen, self.screen_width / 2, self.screen_height / 4)

            results = self.load_results()
            for i, result in enumerate(results):
                self.draw_text(f"{i + 1}. {result:.2f} секунд", self.small_font, self.black, self.screen, self.screen_width / 2, self.screen_height / 3 + i * 40)

            pygame.display.update()

    def game_menu(self):
        menu = True
        while menu:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.background_image_main, (0, 0))
            self.create_button("Начать игру", self.screen_width / 3, self.screen_height / 2, 300, 75, self.dark_blue, self.blue, self.select_units_menu)
            self.create_button("Результаты (Топ-10)", self.screen_width / 3, self.screen_height / 1.5, 300, 75, self.dark_green, self.green, self.show_results)
            self.create_button("Выйти", self.screen_width / 3, self.screen_height / 1.2, 300, 75, self.dark_red, self.red, pygame.quit)

            pygame.display.update()

if __name__ == "__main__":
    menu = GameMenu()
    menu.game_menu()
