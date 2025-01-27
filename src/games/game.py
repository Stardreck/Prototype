from abc import ABC, abstractmethod

import pygame

from managers.debug_manager import DebugManager


class Game(ABC):
    """
    Abstract game base class
    """
    def __init__(self):
        self.is_running = True
        self.debug_manager: DebugManager | None = None

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def handle_movement(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def handle_touch_mouse_down(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def handle_touch_mouse_up(self, event: pygame.event.Event):
        pass
    @abstractmethod
    def handle_touch_mouse_motion(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    def stop(self):
        self.is_running = False
