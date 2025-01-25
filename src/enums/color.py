from enum import Enum


class Color(Enum):
    """Farben als Enum für bessere Lesbarkeit."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DEBUG_BG = (40, 40, 60)
    GAME_BG = (20, 20, 40)
    PLAYER = (255, 60, 60)
    BUTTON_BG = (80, 80, 200)
    BUTTON_HOVER = (100, 100, 220)