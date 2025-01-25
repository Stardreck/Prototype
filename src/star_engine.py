import pathlib
import sys
from typing import Optional

import pygame
from enums.color import Color
from games.game import Game
from star_config import StarConfig


class StarEngine:
    """
    Main engine for the StarDreck game, handling initialization, the main menu, and the main game loop.
    """

    def __init__(self, config: StarConfig):
        """
        Initialize the game engine, set up pygame, and load resources.
        """
        self.config = config
        self._initialize_pygame()
        self._setup_display()
        self._load_resources()

    def _initialize_pygame(self):
        """
        Initialize pygame and set up general settings.
        """
        pygame.init()
        self.width = self.config.width
        self.height = self.config.height
        self.fps = self.config.fps
        self.is_running = True

    def _setup_display(self):
        """
        Set up the display, window title, and clock.
        """
        self.title = self.config.title
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()

    def _load_resources(self):
        """
        Load game resources, such as fonts and directories.
        """
        self.src_dir = pathlib.Path(__file__).resolve().parent.parent

        # Load fonts
        font_path = self.src_dir.joinpath("assets", "fonts", "StarJedi", "Starjedi.ttf")
        self.title_font = pygame.font.Font(str(font_path), 64)
        self.menu_font = pygame.font.SysFont(None, 36)

        # Load background image
        #bg_path = self.src_dir.joinpath("assets", "welcome_screen.png")
        #self.background_image = pygame.image.load(str(bg_path))
        self.background_image =  pygame.image.load(str(self.config.main_menu_background_image))

    def show_main_menu(self) -> str:
        """
        Display the main menu and return the selected option.
        :return: Selected option as a string (e.g., "storygame" or "quit").
        """
        button_width, button_height = 250, 60
        button_x = (self.width - button_width) // 2
        button_y = (self.height - button_height) // 2

        while self.is_running:
            result = self._process_menu_events(button_x, button_y, button_width, button_height)
            if result:
                return result
            self._render_main_menu(button_x, button_y, button_width, button_height)

    def _process_menu_events(self, button_x: int, button_y: int, button_width: int, button_height: int) -> Optional[str]:
        """
        Handle events for the main menu.
        :return: "quit" or "storygame" if a button is clicked.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
                return "quit"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._is_mouse_over_button(event.pos, button_x, button_y, button_width, button_height):
                    return "storygame"

    def _render_main_menu(self, button_x: int, button_y: int, button_width: int, button_height: int) -> None:
        """
        Render the main menu UI.
        :param button_x: X-coordinate of the button.
        :param button_y: Y-coordinate of the button.
        :param button_width: Width of the button.
        :param button_height: Height of the button.
        """
        # Draw background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw title
        title_surface = self.title_font.render("Stardreck", True, Color.WHITE.value)
        title_rect = title_surface.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Draw button
        self._draw_button(button_x, button_y, button_width, button_height)

        pygame.display.flip()

    def _is_mouse_over_button(self, mouse_pos: tuple[int, int], button_x: int, button_y: int, button_width: int, button_height: int) -> bool:
        """
        Check if the mouse is over the button.
        :param mouse_pos: Current mouse position.
        :param button_x: X-coordinate of the button.
        :param button_y: Y-coordinate of the button.
        :param button_width: Width of the button.
        :param button_height: Height of the button.
        :return: True if mouse is over the button, False otherwise.
        """
        mx, my = mouse_pos
        return button_x <= mx <= button_x + button_width and button_y <= my <= button_y + button_height

    def _draw_button(self, button_x: int, button_y: int, button_width: int, button_height: int) -> None:
        """
        Draw the main menu button with hover effect.
        :param button_x: X-coordinate of the button.
        :param button_y: Y-coordinate of the button.
        :param button_width: Width of the button.
        :param button_height: Height of the button.
        """
        mx, my = pygame.mouse.get_pos()
        button_color = Color.BUTTON_HOVER.value if self._is_mouse_over_button((mx, my), button_x, button_y, button_width, button_height) else Color.BUTTON_BG.value

        pygame.draw.rect(self.screen, button_color, (button_x, button_y, button_width, button_height))

        # Draw button text
        text_surface = self.menu_font.render("Reise beginnen", True, Color.WHITE.value)
        text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.screen.blit(text_surface, text_rect)

    def run(self, game: Game) -> None:
        """
        Main game loop that handles events, updates, and rendering.
        :param game: The active game instance.
        """
        while self.is_running and game.is_running:
            delta_time = self.clock.tick(self.fps) / 1000.0
            game.handle_events()
            game.update(delta_time)
            game.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
