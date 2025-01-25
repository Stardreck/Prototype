from abc import ABC, abstractmethod


class Game(ABC):
    """
    Abstract game base class
    """
    def __init__(self):
        self.is_running = True

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    def stop(self):
        self.is_running = False
