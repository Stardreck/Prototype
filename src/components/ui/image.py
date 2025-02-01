import pygame
from components.ui.ui_component import UIComponent

class Image(UIComponent):
    """
    A UI component for displaying an image.

    This component loads an image from a specified path, scales it to the desired size,
    and renders it at the given position.
    """
    def __init__(self, image_path: str, position: tuple[int, int], width: int, height: int):
        """
        :param image_path: Path to the image file.
        :param position: Tuple (x, y) for the image position (position of the top-left corner).
        :param width: Desired width of the image.
        :param height: Desired height of the image.
        """
        self.image_path = image_path
        self.position = position
        self.width = width
        self.height = height
        self.image = None

    def set_image_path(self, path: str):
        self.image_path = path

    def _load_image(self):
        """
        Loads the image and scales it to the specified size.
        If the image cannot be loaded, a placeholder surface is created.
        """
        try:
            self.image = pygame.image.load(self.image_path).convert()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except Exception as e:
            print(f"Error loading image '{self.image_path}': {e}")
            # Create a placeholder surface (magenta) to indicate the error
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 255))

    def draw(self, surface: pygame.Surface):
        self._load_image()
        """
        Draws the image onto the given surface.
        """
        surface.blit(self.image, self.position)

    def handle_event(self, event):
        pass
