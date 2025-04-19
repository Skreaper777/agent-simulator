# utils.py

def gradient_color(value: float, max_value: float) -> tuple:
    ratio = min(1.0, max(0.0, value / max_value)) if max_value > 0 else 0
    green = int(255 * ratio)
    red = 255 - green
    return red, green, 0
