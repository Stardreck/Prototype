# enable type annotations
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # Only imports the below statements during type checking
    from games.game import Game

import sys
import pygame
from managers.view_manager import ViewManager
from src.star_config import StarConfig
from views.intro_view import IntroView
from views.main_view import MainView
from views.settings_view import SettingsView


class StarEngine:
    font: pygame.font.Font | None = None

    def __init__(self):
        self.config: StarConfig | None = StarConfig("Star Temp")

        # Initialize Pygame
        pygame.init()
        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()
        # font settings
        StarEngine.font = pygame.font.SysFont(None, 32)
        # Screen setup
        self.screen_size = (1600, 720)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.config.title)

        # init view manager
        self.view_manager = ViewManager(self.screen)

        # register views
        self.register_views()

        # State variables
        self.is_running = True

    def register_views(self):
        """
        Registers all views with the ViewManager.
        """
        self.view_manager.register_view("intro", IntroView)
        self.view_manager.register_view("main", MainView)
        self.view_manager.register_view("settings", SettingsView)

    def update(self, delta_time: float):
        """
        Updates the game state. This method is called 60 times per second by default.

        Args:
            delta_time (float): The time in seconds since the last update call.
        """
        # TODO: Update game state here
        # Example: Print delta_time for debugging
        # print(f"Delta Time: {delta_time}")
        pass

    def on_draw(self):
        """
        Renders the game content onto the screen. Called whenever the screen needs to be redrawn.
        """
        # Clear the screen with a color (black)
        self.screen.fill((0, 0, 0))

        # TODO: Add drawing code here
        # Example: a simple rectangle
        pygame.draw.rect(self.screen, (0, 255, 0), (100, 100, 200, 150))

        # Update the display
        pygame.display.flip()

    def on_key_press(self, event):
        """
        Handles key press events. Called when a key is pressed.

        Args:
            event (pygame.event.Event): The key press event.
        """
        print(f"Key pressed: {event.key}")

        # ESCAPE Key
        if event.key == pygame.K_ESCAPE:
            self.is_running = False

    def play_intro(self):
        self.view_manager.set_view("intro")
        self.view_manager.render()

    def show_main_menu(self):
        self.view_manager.set_view("main")
        self.view_manager.render()

    def kill(self):
        pygame.quit()
        sys.exit()

    def run(self, game: Game):

        # play the game intro video
        # self.play_intro()
        # display the game main menu, contains own event loop
        self.show_main_menu()
        if not self.is_running:
            self.kill()
        # elf.kill()

        # main game loop
        while self.is_running and game.is_running:
            self.clock.tick(self.config.fps)
            game.handle_events()
            game.update()
            game.draw()
            pygame.display.flip()

        # quit application
        self.kill()

        # main game loop
        # while self.is_running:
        #     # Calculate delta_time
        #     delta_time = self.clock.tick(60) / 1000.0  # 60 FPS, convert milliseconds to seconds
        #
        #     # Event handling
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             self.is_running = False
        #         elif event.type == pygame.KEYDOWN:
        #             self.on_key_press(event)
        #
        #     # Update the game state
        #     self.update(delta_time)
        #
        #     # Render the screen
        #     self.on_draw()
        #
        # # Quit application
        # pygame.quit()
