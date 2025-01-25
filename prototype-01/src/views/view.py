import os

import pygame
import pygame_gui
from pygame import Surface
from pygame_gui import UIManager

from managers.view_manager import ViewManager


class View:
    def __init__(self, screen: Surface, view_manager: ViewManager):
        self.screen: Surface = screen
        self.view_manager: ViewManager = view_manager
        self.theme_path = "theme/gui.json"
        if not os.path.exists(self.theme_path):
            print(f"Theme file could not be found: {self.theme_path}")

        # init pygame GUI Manager
        self.UIManager: UIManager = pygame_gui.UIManager(self.screen.get_size(), theme_path=self.theme_path)

        self.background_image: str | None = None
        self.background_surface: Surface | None = None
        # view state
        self.is_visible = True
        self.clock = pygame.time.Clock()

    def set_background_image(self, image_path: str):
        self.background_image = pygame.image.load(image_path)
        self.background_surface = pygame.transform.scale(self.background_image, self.screen.get_size())

    def render(self):
        pass
