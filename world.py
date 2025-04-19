# world.py (актуальная версия, используется в релизной сборке)

import pygame
import random
from constants import MAP_WIDTH, HEIGHT, FOOD_RADIUS
from agent import Agent

food_items = []


def spawn_food(count=10):
    for _ in range(count):
        x = random.randint(FOOD_RADIUS, MAP_WIDTH - FOOD_RADIUS)
        y = random.randint(FOOD_RADIUS, HEIGHT - FOOD_RADIUS)
        food_items.append(pygame.Vector2(x, y))


def update_food(agents, delta_time, game_speed_multiplier, global_score):
    from constants import BASE_DECREASE_INTERVAL
    updated_food = []

    for agent in agents:
        agent.hunger_timer -= delta_time * 1000 * game_speed_multiplier
        if agent.hunger_timer <= 0:
            if agent.hunger > 80:
                gain = min(5, agent.hunger - 80)
                global_score += gain
            agent.decrease_hunger()
            agent.hunger_timer = BASE_DECREASE_INTERVAL

    for food in food_items:
        eaten = False
        for agent in agents:
            if agent.get_position().distance_to(food) <= 10:  # 10 — радиус взаимодействия
                agent.hunger = 100
                agent.memory["еда"] = agent.memory.get("еда", 0) + 100
                if agent.target_food and agent.target_food == food:
                    agent.memory["зрение"] = agent.memory.get("зрение", 0) + 100
                    agent.target_food = None
                eaten = True
                break
        if not eaten:
            updated_food.append(food)

    food_items.clear()
    food_items.extend(updated_food)
    return global_score
