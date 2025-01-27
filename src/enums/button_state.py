from enum import Enum


class ButtonState(Enum):
    """Farben als Enum für bessere Lesbarkeit."""
    IDLE = 0
    HOVER = 1
    CLICKED = 2