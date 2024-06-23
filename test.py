import pygame
import sys
import time
import json
from OpenGL.GL import *
from OpenGL.GLUT import *

# Инициализация Pygame
pygame.init()

# Размеры окна
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Заголовок окна
pygame.display.set_caption("Меню игры")

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
grey = (100, 100, 100)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
dark_blue = (0, 0, 100)
dark_red = (100, 0, 0)
dark_green = (0, 100, 0)

# Шрифты
font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 30)

# Глобальные переменные для юнитов и результатов
number_of_units = 10
results_file = "results.json"

# Загрузка фоновых изображений
background_image_main = pygame.image.load("C:/klasss/archive/simulation/background_image_main.png")
background_image_main = pygame.transform.scale(background_image_main, (screen_width, screen_height))

background_image_results = pygame.image.load("C:/klasss/archive/simulation/background_image_results.png")
background_image_results = pygame.transform.scale(background_image_results, (screen_width, screen_height))

background_image_units = pygame.image.load("C:/klasss/archive/simulation/background_image_units.png")
background_image_units = pygame.transform.scale(background_image_units, (screen_width, screen_height))

# Загрузка результатов
def load_results():
    try:
        with open(results_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Сохранение результатов
def save_results(results):
    with open(results_file, "w") as file:
        json.dump(results, file)

# Функция для отображения текста на экране
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Функция для создания кнопки
def create_button(text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
            pygame.time.wait(200)  # Задержка для одного клика
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    draw_text(text, small_font, white, screen, x + (width / 2), y + (height / 2))

# Функция для увеличения количества юнитов
def increase_units():
    global number_of_units
    number_of_units = min(100, number_of_units + 1)

# Функция для уменьшения количества юнитов
def decrease_units():
    global number_of_units
    number_of_units = max(1, number_of_units - 1)

# Функция для запуска игры
def start_game():
    global number_of_units
    state = State()
    window = Window(100, 100)
    
    for _ in range(number_of_units):
        state.create_new_object()

    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        glClear(GL_COLOR_BUFFER_BIT)
        window.draw()
        state.show_state()
        for obj in state.state:
            state.update_object_position(obj)

        pygame.display.flip()
        pygame.time.wait(10)
    
        if not state.has_humans():  # Проверка на окончание игры
            running = False

    end_time = time.time()
    game_duration = end_time - start_time
    save_result(game_duration)

# Сохранение результата
def save_result(duration):
    results = load_results()
    results.append(duration)
    results.sort(reverse=True)
    results = results[:10]
    save_results(results)

# Функция для выбора количества юнитов
def select_units_menu():
    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_image_units, (0, 0))
        create_button("Выйти в главное меню", screen_width / 2 - 150, 50, 300, 50, dark_red, red, game_menu)
        draw_text("Выберите количество юнитов", font, white, screen, screen_width / 2, screen_height / 4)
        draw_text(f"{number_of_units}", font, white, screen, screen_width / 2, screen_height / 2)

        create_button("-", screen_width / 2 - 150, screen_height / 2 - 25, 50, 50, dark_red, red, decrease_units)
        create_button("+", screen_width / 2 + 100, screen_height / 2 - 25, 50, 50, dark_green, green, increase_units)
        create_button("Начать", screen_width / 2 - 100, screen_height / 1.2, 200, 50, dark_blue, blue, start_game)

        pygame.display.update()

# Функция для отображения результатов
def show_results():
    showing = True
    while showing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing = False

        screen.blit(background_image_results, (0, 0))
        draw_text("Топ 10 результатов", font, white, screen, screen_width / 2, screen_height / 4)

        results = load_results()
        for i, result in enumerate(results):
            draw_text(f"{i + 1}. {result:.2f} секунд", small_font, black, screen, screen_width / 2, screen_height / 3 + i * 40)

        pygame.display.update()

# Основная функция меню
def game_menu():
    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_image_main, (0, 0))
        #draw_text("Главное Меню", font, black, screen, screen_width / 2, screen_height / 4)

        create_button("Начать игру", screen_width / 3, screen_height / 2, 300, 75, dark_blue, blue, select_units_menu)
        create_button("Результаты (Топ-10)", screen_width / 3, screen_height / 1.5, 300, 75, dark_green, green, show_results)
        create_button("Выйти", screen_width / 3, screen_height / 1.2, 300, 75, dark_red, red, pygame.quit)

        pygame.display.update()

game_menu()