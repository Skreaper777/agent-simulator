# agent.py
import pygame
import math
import random
from constants import *

class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hunger = random.randint(50, 100)  # сытость
        self.satisfaction = self.hunger  # стартовое равенство
        self.direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.target_direction = self.direction.copy()
        self.last_direction_change = pygame.time.get_ticks()
        self.birth_time = pygame.time.get_ticks()
        self.memory = {"log": []}  # 👈 добавляем лог удовлетворения
        self.lifetime = 0.0
        self.decrease_timer = random.uniform(0, 5) * 1000
        self.target_food = None

        self.hunger = 100
        self.hunger_timer = random.uniform(0, 5) * 1000
        self.satisfaction = self.hunger

    def get_vision_params(self):
        vision_experience = self.memory.get("зрение", 0)
        level = min(vision_experience // 500, 4)
        length_multiplier = 1.0 + level * 0.25
        angle_multiplier = 1.0 + level * 0.25
        return VISION_DISTANCE * length_multiplier, VISION_ANGLE * angle_multiplier

    def update(self, delta_time):
        self.lifetime += delta_time
        self.update_satisfaction_from_hunger()

        if self.hunger > 80:
            return

        self.look_for_food()
        self.avoid_walls()

        if self.hunger <= 80 and not self.target_food:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_direction_change >= 1000:
                self.target_direction = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
                self.last_direction_change = current_time

        rotate_speed = 4.0
        self.direction = self.direction.lerp(self.target_direction, min(1.0, rotate_speed * delta_time)).normalize()

        speed = 30 if self.hunger < 50 else 15
        dx = self.direction.x * speed * delta_time
        dy = self.direction.y * speed * delta_time
        self.x = max(AGENT_RADIUS, min(MAP_WIDTH - AGENT_RADIUS, self.x + dx))
        self.y = max(AGENT_RADIUS, min(HEIGHT - AGENT_RADIUS, self.y + dy))

    def update_satisfaction_from_hunger(self):
        previous = self.satisfaction
        self.satisfaction = min(100, self.hunger)
        delta = self.satisfaction - previous
        if delta != 0:
            reason = "голод" if delta < 0 else "восстановление"
            self.memory.setdefault("log", []).append((self.lifetime, reason, delta))
            if len(self.memory["log"]) > 15:
                self.memory["log"] = self.memory["log"][-15:]

    def decrease_hunger(self):
        if self.hunger > 0:
            self.hunger = max(0, self.hunger - 5)

    def avoid_walls(self):
        vision_distance, _ = self.get_vision_params()
        buffer = vision_distance / 2
        changed = False

        if self.x - buffer < 0:
            self.target_direction.x = abs(self.direction.x)
            changed = True
        elif self.x + buffer > MAP_WIDTH:
            self.target_direction.x = -abs(self.direction.x)
            changed = True

        if self.y - buffer < 0:
            self.target_direction.y = abs(self.direction.y)
            changed = True
        elif self.y + buffer > HEIGHT:
            self.target_direction.y = -abs(self.direction.y)
            changed = True

        if changed:
            self.target_direction = self.target_direction.normalize()

    def look_for_food(self):
        from world import food_items

        position = pygame.Vector2(self.x, self.y)
        forward = self.direction
        self.target_food = None
        vision_distance, angle = self.get_vision_params()

        for food in food_items:
            vec_to_food = food - position
            dist = vec_to_food.length()
            if dist > vision_distance:
                continue
            angle_to_food = forward.angle_to(vec_to_food)
            if abs(angle_to_food) <= angle / 2:
                self.target_food = food
                self.target_direction = vec_to_food.normalize()
                break

    def get_position(self):
        return pygame.Vector2(self.x, self.y)

    def get_lifetime(self):
        return self.lifetime