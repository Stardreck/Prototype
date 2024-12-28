import json

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from src.star_config import StarConfig


class StarEngine:
    def __init__(self, screen_manager: ScreenManager):
        self.screen_manager: ScreenManager = screen_manager
        self.config: StarConfig | None = None

        self.load_engine_config()

    def load_engine_config(self):
        with open("data/star_config.json", 'r') as file:
            data = json.load(file)
        self.config: StarConfig = StarConfig(data["title"])

    def add_screen(self, screen):
        self.screen_manager.add_widget(screen)

    def set_screen(self, screen_name):
        self.screen_manager.current = screen_name

    def update(self, delta_time: float):
        """
        Updates the game state. This method is called 60 times per second by default.
        Args:
            delta_time (float): The time in seconds since the last update call.
        """
        # ToDo, update game state here
        # print(deltaTime)
        pass

    def on_key_press(self, symbol, modifiers):
        print("star_engine on_key_press called.", symbol, modifiers)
        pass

    def run(self):
        # Starts the main game loop and schedules the update method for 60 frames per second.
        # calls the update method 60 times per second
        Clock.schedule_interval(self.update, 1 / 60.0)

        # Bind key press events
        Window.bind(on_key_down=self.on_key_press)
