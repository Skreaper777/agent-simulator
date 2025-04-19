# constants.py
"""
✅ Централизованные константы для проекта Agent Simulator
- Цвета
- Радиусы
- Размеры экрана и меню
- Параметры агентов
- Стоимости
- Интервалы
"""

# 🎨 Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FOOD_COLOR = (255, 0, 0)
AGENT_COLOR_DEFAULT = (0, 255, 0)
VISION_COLOR = (0, 150, 255, 50)
MODAL_BG = (50, 50, 50)
BUTTON_COLOR = (100, 100, 100)
BUTTON_HOVER_COLOR = (150, 150, 150)
BUTTON_ACTIVE_COLOR = (0, 150, 0)
CLOSE_COLOR = (180, 50, 50)

# 📏 Размеры экрана и меню
MAP_WIDTH = 820
HEIGHT = 600
MENU_WIDTH = 1000
WIDTH = MAP_WIDTH + MENU_WIDTH

# ⚪ Радиусы
AGENT_RADIUS = 10
FOOD_RADIUS = 4
BORDER_THICKNESS = 5

# 👁️‍🗨️ Зрение агентов
VISION_DISTANCE = AGENT_RADIUS * 4
VISION_ANGLE = 30

# ⏲️ Интервалы и таймеры
BASE_DECREASE_INTERVAL = 5000
SATISFACTION_INTERVAL = 5.0  # секунды между оценками «моего удовольствия»

# 💰 Стоимости
AGENT_COST = 100
FOOD_COST = 5