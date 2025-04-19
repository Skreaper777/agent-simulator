# ui.py
# 💾 Актуальная версия ui.py, используется в релизной сборке

import pygame
import math
from constants import *
from utils import gradient_color

menu_button_rect = pygame.Rect(10, 10, 120, 30)
menu_modal_rect = pygame.Rect(10, 50, 200, 300)


def draw_speed_buttons(screen, font, button_rects, active_label):
    for rect, label, _ in button_rects:
        color = BUTTON_ACTIVE_COLOR if label == active_label else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)
        text = font.render(label, True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))


def draw_add_buttons(screen, font, button_rects, active_mode, score_y):
    for rect, label, mode, cost in button_rects:
        color = BUTTON_ACTIVE_COLOR if active_mode == mode else BUTTON_COLOR
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, WHITE, rect, 1)
        text = font.render(f"{label} ({cost})", True, WHITE)
        screen.blit(text, text.get_rect(center=rect.center))


def draw_score(screen, score):
    score_font = pygame.font.SysFont(None, 28)
    text = score_font.render(f"Счёт игры: {score}", True, WHITE)
    pos = (MAP_WIDTH + 20, HEIGHT - 40)
    screen.blit(text, pos)
    return pos[1]


def draw_menu_button(screen, font, mouse_pos, is_active):
    pygame.draw.rect(screen, BUTTON_HOVER_COLOR if menu_button_rect.collidepoint(mouse_pos) else BUTTON_COLOR,
                     menu_button_rect)
    pygame.draw.rect(screen, WHITE, menu_button_rect, 2)
    text = font.render("Меню", True, WHITE)
    screen.blit(text, (menu_button_rect.x + 30, menu_button_rect.y + 5))
    # return menu_button_rect.collidepoint(mouse_pos)



def draw_menu_modal(screen, font, mouse_pos, current_mode, current_add_mode):
    """Draw the left‑top modal and handle one‑click selection.

    Returns:
        tuple(color_mode, add_mode)
    """
    pygame.draw.rect(screen, MODAL_BG, menu_modal_rect)
    pygame.draw.rect(screen, WHITE, menu_modal_rect, 2)

    color_buttons = [
        ("Удовлетворение", "satisfaction"),
        ("Время жизни", "lifetime"),
        ("Еда", "memory_eat"),
        ("Зрение", "memory_vision"),
    ]

    add_buttons = [
        ("Добавить еду", "food", FOOD_COST),
        ("Купить агента", "agent", AGENT_COST),
    ]

    # ---------- debounce click ----------
    if not hasattr(draw_menu_modal, "_prev_pressed"):
        draw_menu_modal._prev_pressed = False
    mouse_pressed = pygame.mouse.get_pressed()[0]
    clicked_now = mouse_pressed and not draw_menu_modal._prev_pressed
    draw_menu_modal._prev_pressed = mouse_pressed

    new_mode = current_mode
    new_add_mode = current_add_mode

    # ----- draw color buttons -----
    for idx, (label, mode) in enumerate(color_buttons):
        rect = pygame.Rect(menu_modal_rect.x + 10,
                           menu_modal_rect.y + 10 + idx * 40,
                           180, 30)
        pygame.draw.rect(screen,
                         BUTTON_ACTIVE_COLOR if current_mode == mode else BUTTON_COLOR,
                         rect)
        pygame.draw.rect(screen, WHITE, rect, 1)
        text = font.render(label, True, WHITE)
        screen.blit(text, (rect.x + 10, rect.y + 5))

        if clicked_now and rect.collidepoint(mouse_pos):
            new_mode = mode

    # ----- draw add buttons -----
    start_y = menu_modal_rect.y + 10 + len(color_buttons) * 40 + 20
    for idx, (label, mode, cost) in enumerate(add_buttons):
        rect = pygame.Rect(menu_modal_rect.x + 10,
                           start_y + idx * 40,
                           180, 30)
        pygame.draw.rect(screen,
                         BUTTON_ACTIVE_COLOR if current_add_mode == mode else BUTTON_COLOR,
                         rect)
        pygame.draw.rect(screen, WHITE, rect, 1)
        text = font.render(f"{label} ({cost})", True, WHITE)
        screen.blit(text, (rect.x + 10, rect.y + 5))

        if clicked_now and rect.collidepoint(mouse_pos):
            if current_add_mode == mode:
                new_add_mode = None
            else:
                new_add_mode = mode

    return new_mode, new_add_mode
def draw_agent_modal(screen, font, agent, modal_rect, close_rect):
    pygame.draw.rect(screen, CLOSE_COLOR, close_rect)
    pygame.draw.line(screen, WHITE, close_rect.topleft, close_rect.bottomright, 2)
    pygame.draw.line(screen, WHITE, close_rect.topright, close_rect.bottomleft, 2)

    lines = [
        "Информация об агенте:",
        f"Удовлетворение: {int(agent.satisfaction)}",
        f"Сытость: {int(agent.hunger)}",
        f"Время жизни: {agent.lifetime:.1f} сек",
        "Лог памяти (последние 15):"
    ]

    log = agent.memory.get("log", [])[-15:]
    for entry in log:
        if isinstance(entry, tuple) and len(entry) == 3:
            t, reason, delta = entry
            t, param, delta = entry
            action = "уменьш." if delta < 0 else "увелич."
            lines.append(f"{t:.1f}s — {param} {action} на {abs(delta)} ед.")
        else:
            lines.append(f"Неверный формат памяти: {entry}")

    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        screen.blit(text, (modal_rect.x, modal_rect.y + 10 + i * 25))


def draw_agent(screen, agent, color_mode, max_lifetime):
    if color_mode == "satisfaction":
        inner_color = gradient_color(agent.satisfaction, 100)
    elif color_mode == "lifetime":
        inner_color = gradient_color(agent.lifetime, max_lifetime)
    elif color_mode == "memory_eat":
        value = agent.memory.get("еда", 0)
        inner_color = gradient_color(value, 300)
    elif color_mode == "memory_vision":
        value = agent.memory.get("зрение", 0)
        inner_color = gradient_color(value, 300)
    else:
        inner_color = AGENT_COLOR_DEFAULT

    border_color = gradient_color(agent.satisfaction, 100)
    pygame.draw.circle(screen, border_color, (int(agent.x), int(agent.y)), AGENT_RADIUS + BORDER_THICKNESS)
    pygame.draw.circle(screen, inner_color, (int(agent.x), int(agent.y)), AGENT_RADIUS)
    draw_vision(screen, agent)


def draw_vision(screen, agent):
    center = pygame.Vector2(agent.x, agent.y)
    direction = agent.direction.angle_to(pygame.Vector2(1, 0))
    vision_distance, angle = agent.get_vision_params()
    left_angle = math.radians(direction - angle / 2)
    right_angle = math.radians(direction + angle / 2)
    left_vector = pygame.Vector2(math.cos(left_angle), -math.sin(left_angle)) * vision_distance
    right_vector = pygame.Vector2(math.cos(right_angle), -math.sin(right_angle)) * vision_distance
    points = [center, center + left_vector, center + right_vector]
    pygame.draw.polygon(screen, (0, 100, 255), points, 1)
    for vec in [left_vector, right_vector]:
        end_pos = (int(center.x + vec.x), int(center.y + vec.y))
        pygame.draw.circle(screen, (0, 100, 255), end_pos, 3)