import pygame
import random
import sys
import os

pygame.init()
pygame.mixer.init()

eat_sound = pygame.mixer.Sound("eat.wav")
lose_sound = pygame.mixer.Sound("lose.wav")


pygame.mixer.music.load("muzyka.mp3")
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)         

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
background_menu = pygame.image.load("tło_menu.png").convert()
background_menu = pygame.transform.scale(background_menu, (WIDTH, HEIGHT))
background_rest = pygame.image.load("tło_rest.png").convert()
background_rest = pygame.transform.scale(background_rest, (WIDTH, HEIGHT))
background_end = pygame.image.load("tło_end.png").convert()
background_end = pygame.transform.scale(background_end, (WIDTH, HEIGHT))
background_game = pygame.image.load("tło_game.png").convert()
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
CELL_SIZE = 60

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)
button_font = pygame.font.SysFont(None, 28)

difficulty_levels = {'Łatwy': 7, 'Standardowy': 10, 'Trudny': 15}
difficulty_names = list(difficulty_levels.keys())
difficulty_index = 1
fps = difficulty_levels[difficulty_names[difficulty_index]]

snake_colors = {'Zielony': GREEN, 'Niebieski': BLUE, 'Czarny': BLACK}
color_names = list(snake_colors.keys())
color_index = 0
snake_color = snake_colors[color_names[color_index]]

highscores_file = "highscores.txt"
if not os.path.exists(highscores_file):
    with open(highscores_file, 'w', encoding='utf-8', errors='ignore') as f:
        for level in difficulty_names:
            f.write(f"{level}:0\n")

def load_highscores():
    scores = {name: 0 for name in difficulty_names}
    with open(highscores_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            try:
                name, score = line.strip().split(":")
                scores[name] = int(score)
            except:
                continue
    return scores

def save_highscore(level, score):
    scores = load_highscores()
    if score > scores[level]:
        scores[level] = score
        with open(highscores_file, 'w') as f:
            for name in difficulty_names:
                f.write(f"{name}:{scores[name]}\n")

def draw_button(rect, text, font, bg_color=LIGHT_GRAY, text_color=BLACK):
    pygame.draw.rect(screen, bg_color, rect)
    pygame.draw.rect(screen, DARK_GRAY, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (230, 230, 230), (x, 20), (x, HEIGHT))
    for y in range(20, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (230, 230, 230), (0, y), (WIDTH, y))

def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, snake_color, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

def get_random_food_position(snake):
    while True:
        x = random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE
        y = random.randrange(60 // CELL_SIZE, HEIGHT // CELL_SIZE) * CELL_SIZE  
        pos = [x, y]
        if pos not in snake:
            return pos

def game():
    global fps, snake_color
    snake = [[CELL_SIZE * 2, CELL_SIZE * 2], [CELL_SIZE, CELL_SIZE * 2], [0, CELL_SIZE * 2]]
    direction = 'RIGHT'
    food = get_random_food_position(snake)
    score = 0
    lives = 3

    while lives > 0:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and direction != 'DOWN':
            direction = 'UP'
        if keys[pygame.K_DOWN] and direction != 'UP':
            direction = 'DOWN'
        if keys[pygame.K_LEFT] and direction != 'RIGHT':
            direction = 'LEFT'
        if keys[pygame.K_RIGHT] and direction != 'LEFT':
            direction = 'RIGHT'

        # Ruch głowy węża
        head = snake[0].copy()
        if direction == 'UP':
            head[1] -= CELL_SIZE
        elif direction == 'DOWN':
            head[1] += CELL_SIZE
        elif direction == 'LEFT':
            head[0] -= CELL_SIZE
        elif direction == 'RIGHT':
            head[0] += CELL_SIZE

        # Sprawdzenie kolizji
        if (
            head[0] < 0 or head[0] >= WIDTH or
            head[1] < 60 or head[1] >= HEIGHT or
            head in snake
        ):
            lives -= 1
            lose_sound.play()  # Dźwięk przegranej życia
            snake = [[CELL_SIZE * 2, CELL_SIZE * 2], [CELL_SIZE, CELL_SIZE * 2], [0, CELL_SIZE * 2]]
            direction = 'RIGHT'
            food = get_random_food_position(snake)
            continue

        snake.insert(0, head)

        # Zjedzenie jedzenia
        if head == food:
            score += 1
            eat_sound.play()  # Dźwięk zjedzenia jabłka
            food = get_random_food_position(snake)
        else:
            snake.pop()

        # Rysowanie tła i gry
        screen.blit(background_game, (0, 0))
        pygame.draw.rect(screen, (200, 200, 200), (0, 0, WIDTH, 60))  # Szary pasek

        draw_snake(snake)
        draw_food(food)

        score_text = font.render(f"Wynik: {score}", True, BLACK)
        screen.blit(score_text, (10, 2))

        lives_text = font.render(f"Życia: {lives}", True, BLACK)
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 2))

        pygame.display.flip()

    # Koniec gry
    save_highscore(difficulty_names[difficulty_index], score)
    screen.blit(background_end, (0, 0))
    pygame.display.flip()
    pygame.time.wait(3000)

# --- Ekrany dodatkowe ---
# --- Ekran z zasadami gry ---
def show_rules():
    back_button = pygame.Rect(20, HEIGHT - 60, 150, 40)
    rules = [
        "Zasady gry Snake:",
        "- Steruj wężem strzałkami.",
        "- Zbieraj czerwone jabłka, aby rosnąć i zdobywać punkty.",
        "- Nie uderzaj w ściany ani w własny ogon.",
        "- Im więcej punktów, tym trudniej!",
        "",
        "Powodzenia!"
    ]

    rules_font = pygame.font.SysFont(None, 40) 
    line_height = rules_font.get_height() + 10
    total_height = line_height * len(rules)
    start_y = (HEIGHT - total_height) // 2

    while True:
        screen.blit(background_rest, (0, 0))

        for i, line in enumerate(rules):
            text_surface = rules_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, start_y + i * line_height))
            screen.blit(text_surface, text_rect)

        draw_button(back_button, "POWRÓT", small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)

# --- Ekran z konfiguracją gry ---
def show_config():
    global difficulty_index, fps, color_index, snake_color

    back_button = pygame.Rect(20, HEIGHT - 60, 150, 40)
    diff_slider_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//3, 300, 30)
    color_slider_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 30)

    dragging_diff = False
    dragging_color = False

    while True:
        screen.blit(background_rest, (0, 0))

        diff_text = font.render(f"Trudność: {difficulty_names[difficulty_index]}", True, WHITE)
        screen.blit(diff_text, (diff_slider_rect.x, diff_slider_rect.y - 30))

        color_text = font.render(f"Kolor węża: {color_names[color_index]}", True, WHITE)
        screen.blit(color_text, (color_slider_rect.x, color_slider_rect.y - 30))

        pygame.draw.rect(screen, WHITE, diff_slider_rect, 2)
        pygame.draw.rect(screen, WHITE, color_slider_rect, 2)

        diff_pos = diff_slider_rect.x + (difficulty_index / (len(difficulty_names) - 1)) * diff_slider_rect.width
        pygame.draw.circle(screen, WHITE, (int(diff_pos), diff_slider_rect.centery), 10)

        color_pos = color_slider_rect.x + (color_index / (len(color_names) - 1)) * color_slider_rect.width
        pygame.draw.circle(screen, WHITE, (int(color_pos), color_slider_rect.centery), 10)

        draw_button(back_button, "POWRÓT", small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return
                if diff_slider_rect.collidepoint(event.pos):
                    dragging_diff = True
                if color_slider_rect.collidepoint(event.pos):
                    dragging_color = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging_diff = False
                dragging_color = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging_diff:
                    relative_x = event.pos[0] - diff_slider_rect.x
                    relative_x = max(0, min(relative_x, diff_slider_rect.width))
                    new_index = round((relative_x / diff_slider_rect.width) * (len(difficulty_names) - 1))
                    if new_index != difficulty_index:
                        difficulty_index = new_index
                        fps = difficulty_levels[difficulty_names[difficulty_index]]
                if dragging_color:
                    relative_x = event.pos[0] - color_slider_rect.x
                    relative_x = max(0, min(relative_x, color_slider_rect.width))
                    new_index = round((relative_x / color_slider_rect.width) * (len(color_names) - 1))
                    if new_index != color_index:
                        color_index = new_index
                        snake_color = snake_colors[color_names[color_index]]

        pygame.display.flip()
        clock.tick(30)

# --- Ekran z najlepszymi wynikami ---
def show_highscores():
    back_button = pygame.Rect(20, HEIGHT - 60, 150, 40)
    title_font = pygame.font.SysFont(None, 48)     
    score_font = pygame.font.SysFont(None, 36)      
    while True:
        screen.blit(background_rest, (0, 0))
        scores = load_highscores()

        title_height = title_font.size("NAJLEPSZE WYNIKI")[1]
        score_height = score_font.get_height()
        total_height = title_height + (len(difficulty_names) * score_height) + ((len(difficulty_names) + 1) * 10)  
        start_y = (HEIGHT - total_height) // 2

        title = title_font.render("NAJLEPSZE WYNIKI", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH // 2, start_y + title_height // 2))
        screen.blit(title, title_rect)

        for i, level in enumerate(difficulty_names):
            score_text = score_font.render(f"{level}: {scores[level]}", True, WHITE)
            y = start_y + title_height + 10 + i * (score_height + 10) + score_height // 2
            score_rect = score_text.get_rect(center=(WIDTH // 2, y))
            screen.blit(score_text, score_rect)

        draw_button(back_button, "POWRÓT", small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)

# --- Ekran o autorze ---
def show_about_author():
    back_button = pygame.Rect(20, HEIGHT - 60, 150, 40)
    about_lines = [
        "Autor: Filip Wójcicki",
        "Motywacja: Ta gra jest moim pierwszym",
        "większym projektem w Pythonie,który",
        "stworzyłem z pasją i zaangażowaniem.",
        "Mam nadzieję, że sprawi Ci tyle radości,",
        "co mi przy jej tworzeniu.",
        "W planach mam dalsze tworzenie ",
        "bardziej rozbudowanych gier."
    ]

    about_font = pygame.font.SysFont(None, 40)  
    line_height = about_font.get_height() + 10
    total_height = line_height * len(about_lines)
    start_y = (HEIGHT - total_height) // 2

    while True:
        screen.blit(background_rest, (0, 0))

        for i, line in enumerate(about_lines):
            text_surface = about_font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, start_y + i * line_height))
            screen.blit(text_surface, text_rect)

        draw_button(back_button, "POWRÓT", small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    return

        pygame.display.flip()
        clock.tick(30)

# --- Menu główne ---
def main_menu():
    button_count = 4
    button_width = WIDTH // button_count - 15  
    button_height = 40

    start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 10, 200, 50)
    exit_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 40) 

    buttons_bottom_y = HEIGHT - 60
    rules_button = pygame.Rect(10, buttons_bottom_y, button_width, button_height)
    config_button = pygame.Rect(rules_button.right + 10, buttons_bottom_y, button_width, button_height)
    scores_button = pygame.Rect(config_button.right + 10, buttons_bottom_y, button_width, button_height)
    about_button = pygame.Rect(scores_button.right + 10, buttons_bottom_y, button_width, button_height)

    while True:
        screen.blit(background_menu, (0, 0))


        pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, 20))
        info_text = small_font.render(f"Trudność: {difficulty_names[difficulty_index]}    Kolor: {color_names[color_index]}", True, BLACK)
        screen.blit(info_text, (10, 2))

        draw_button(start_button, "START", font)
        draw_button(exit_button, "KONIEC GRY", small_font)  
        draw_button(rules_button, "ZASADY GRY", button_font)
        draw_button(config_button, "KONFIGURACJA", button_font)
        draw_button(scores_button, "NAJLEPSZE WYNIKI", button_font)
        draw_button(about_button, "O AUTORZE", button_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    game()
                elif exit_button.collidepoint(event.pos):  
                    pygame.quit()
                    sys.exit()
                elif rules_button.collidepoint(event.pos):
                    show_rules()
                elif config_button.collidepoint(event.pos):
                    show_config()
                elif scores_button.collidepoint(event.pos):
                    show_highscores()
                elif about_button.collidepoint(event.pos):
                    show_about_author()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main_menu()
