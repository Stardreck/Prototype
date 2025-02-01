from abc import ABC, abstractmethod


class UIComponent(ABC):
    """
    A base class for all UI components. Defines a common interface
    for drawing and (optionally) handling events.
    """
    @abstractmethod
    def draw(self, surface):
        """
        Draw the component onto the given surface.
        Override this method in child classes.
        """
        raise NotImplementedError("draw() must be implemented by subclasses.")

    @abstractmethod
    def handle_event(self, event):
        """
        Handle specific events (e.g., mouse clicks, keyboard).
        Not all components require event handling, so it's optional.
        """
        pass