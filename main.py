# main.py — Актуальная релизная версия
# Исходник обновлён на основе архива 2024-04-18 и подчинён правилу:
# «Точное совпадение имён и регистра переменных с архивом»

# 🔒 Жёсткое правило работы с архивами проекта, которые я загружаю тебе в сообщении:
# Перед любыми изменениями в коде:
# 1. ОТКРЫТЬ и ПРОВЕРИТЬ вручную каждый *.py файл (никаких догадок).
# 2. СОХРАНЯТЬ точные ИМЕНА переменных и регистр без изменений.
# 3. НЕ ИСПОЛЬЗОВАТЬ старые холсты или шаблоны — только последний присланный архив.
# 4. ПОЛНАЯ синхронизация между модулями (аргументы, функции и поведение).
# Архив — единственный источник правды. 📌

# 🔒 Жёсткое правило работы с архивами проекта, которые я загружу тебе в сообщении
# 1. ОТКРЫТЬ и ПРОВЕРИТЬ вручную каждый файл из архива (*.py) без исключений
# 2. СОХРАНЯТЬ точные ИМЕНА переменных и регистр без изменений
# 3. НЕ ИСПОЛЬЗОВАТЬ старые холсты или шаблоны — только последний присланный архив
# 4. ПОЛНАЯ синхронизация параметров и логики между модулями
# Архив — единственный источник правды. 📌

# 🔒 Жёсткое правило работы с архивами проекта, которые я загружу тебе в сообщении
# 1. ОТКРЫТЬ и ПРОВЕРИТЬ вручную каждый файл из архива (*.py) без исключений
# 2. СОХРАНЯТЬ точные ИМЕНА переменных и регистр без изменений
# 3. НЕ ИСПОЛЬЗАТЬ старые холсты или шаблоны — только последний присланный архив
# 4. ПОЛНАЯ синхронизация параметров и логики между модулями
# Архив — единственный источник правды. 📌

import pygame
import sys
import random

from constants import *
from agent import Agent
import world
from ui import (
    draw_speed_buttons,
    
    draw_score,
    draw_menu_button,
    draw_menu_modal,
    draw_agent_modal,
    draw_agent,
    menu_button_rect  # Добавлен импорт
)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF, vsync=1)
pygame.display.set_caption("Симулятор агента")

font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

agents = [Agent(MAP_WIDTH // 2, HEIGHT // 2)]
selected_agent = None
show_agent_modal = False
show_menu_modal = False
color_mode = "satisfaction"

game_speed_multiplier = 1.0
previous_speed_multiplier = 1.0
active_speed_label = "1x"
global_score = 0
add_mode = None

speed_buttons = [
    {"label": "Пауза", "multiplier": 0.0},
    {"label": "0.5x", "multiplier": 0.5},
    {"label": "1x", "multiplier": 1.0},
    {"label": "3x", "multiplier": 3.0},
    {"label": "9x", "multiplier": 9.0},
]

speed_button_rects = []
button_width = 80
button_height = 30
spacing = 10
start_x = MAP_WIDTH // 2 - ((button_width + spacing) * len(speed_buttons) // 2)
start_y = HEIGHT - 50
for i, btn in enumerate(speed_buttons):
    rect = pygame.Rect(start_x + i * (button_width + spacing), start_y, button_width, button_height)
    speed_button_rects.append((rect, btn["label"], btn["multiplier"]))

agent_modal_rect = pygame.Rect(MAP_WIDTH + 20, 20, MENU_WIDTH - 40, 400)
close_button_rect = pygame.Rect(agent_modal_rect.right - 25, agent_modal_rect.y + 5, 20, 20)

while True:
    delta_raw = clock.tick(60)
    delta_time = delta_raw / 1000.0
    mouse_pos = pygame.mouse.get_pos()
    max_lifetime = max([a.lifetime for a in agents], default=1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_agent_modal and close_button_rect.collidepoint(mouse_pos):
                show_agent_modal = False
                selected_agent = None
            else:
                for agent in agents:
                    dx = mouse_pos[0] - agent.x
                    dy = mouse_pos[1] - agent.y
                    if dx ** 2 + dy ** 2 <= AGENT_RADIUS ** 2:
                        selected_agent = agent
                        show_agent_modal = True
                        break

            if menu_button_rect.collidepoint(mouse_pos):
                show_menu_modal = not show_menu_modal

            for rect, label, multiplier in speed_button_rects:
                if rect.collidepoint(mouse_pos):
                    if label == "Пауза":
                        if game_speed_multiplier == 0.0:
                            game_speed_multiplier = previous_speed_multiplier
                            active_speed_label = next((b["label"] for b in speed_buttons if b["multiplier"] == game_speed_multiplier), "1x")
                        else:
                            previous_speed_multiplier = game_speed_multiplier
                            game_speed_multiplier = 0.0
                            active_speed_label = "Пауза"
                    else:
                        game_speed_multiplier = multiplier
                        previous_speed_multiplier = multiplier
                        active_speed_label = label


            if mouse_pos[0] < MAP_WIDTH:
                if add_mode == "food" and global_score >= FOOD_COST:
                    world.food_items.append(pygame.Vector2(mouse_pos[0], mouse_pos[1]))
                    global_score -= FOOD_COST
                elif add_mode == "agent" and global_score >= AGENT_COST:
                    x, y = mouse_pos[0], mouse_pos[1]
                    agents.append(Agent(x, y))
                    global_score -= AGENT_COST

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                x = random.randint(AGENT_RADIUS, MAP_WIDTH - AGENT_RADIUS)
                y = random.randint(AGENT_RADIUS, HEIGHT - AGENT_RADIUS)
                agents.append(Agent(x, y))
            elif event.key == pygame.K_f:
                world.spawn_food()
            elif event.key == pygame.K_SPACE:
                if game_speed_multiplier == 0.0:
                    game_speed_multiplier = previous_speed_multiplier
                    active_speed_label = next((b["label"] for b in speed_buttons if b["multiplier"] == game_speed_multiplier), "1x")
                else:
                    previous_speed_multiplier = game_speed_multiplier
                    game_speed_multiplier = 0.0
                    active_speed_label = "Пауза"

    if game_speed_multiplier > 0:
        for agent in agents:
            agent.update(delta_time * game_speed_multiplier)
        global_score = world.update_food(agents, delta_time, game_speed_multiplier, global_score)

        agents = [a for a in agents if a.satisfaction > 0]
        if selected_agent and selected_agent.satisfaction <= 0:
            show_agent_modal = False
            selected_agent = None

    screen.fill(BLACK)

    for food in world.food_items:
        pygame.draw.circle(screen, FOOD_COLOR, (int(food.x), int(food.y)), FOOD_RADIUS)

    for agent in agents:
        draw_agent(screen, agent, color_mode, max_lifetime)

    draw_menu_button(screen, font, mouse_pos, show_menu_modal)

    if show_menu_modal:
        color_mode, add_mode = draw_menu_modal(screen, font, mouse_pos, color_mode, add_mode)

    if show_agent_modal and selected_agent:
        draw_agent_modal(screen, font, selected_agent, agent_modal_rect, close_button_rect)

    draw_speed_buttons(screen, font, speed_button_rects, active_speed_label)
    draw_score(screen, global_score)

    pygame.display.flip()