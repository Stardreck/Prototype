import json

import pyglet
from kivy.uix.screenmanager import ScreenManager

from src.scenes.scene import Scene
from src.scenes.story_scene import StoryScene
from src.star_config import StarConfig


class StarEngine:
    def __init__(self, screen_manager: ScreenManager):
        self.screen_manager: ScreenManager = screen_manager
        self.config: StarConfig | None = None
        self.load_config_from_json()
        self.window: pyglet.window.Window = pyglet.window.Window(width=800, height=600, caption=self.config.title)
        self.window.push_handlers(self)
        self.current_scene: Scene | None = None
        self.scenes: list[StoryScene] = self.load_scenes_from_json("data/scenes.json")

        # pyglet options
        pyglet.options.search_local_libs = True

    def load_config_from_json(self):
        with open("data/star_config.json", 'r') as file:
            data = json.load(file)
        self.config: StarConfig = StarConfig(data["title"])

    def load_scenes_from_json(self, json_file):
        scenes = []
        try:
            with open(json_file, 'r') as file:
                data = json.load(file)
            for scene_data in data:
                scene = StoryScene(
                    id=scene_data["id"],
                    game_id=scene_data["game_id"],
                    background=scene_data["background"],
                    text=scene_data["text"]
                )
                scene.load_assets()
                scenes.append(scene)
        except FileNotFoundError:
            print("scenes not found")
        finally:
            return scenes

    """ 
    Updates the game state. This method is called 60 times per second by default.
    
    Args:
        delta_time (float): The time in seconds since the last update call.
    """

    def update(self, delta_time: float):
        # ToDo, update game state here
        # print(deltaTime)
        pass

    """
    Renders the game content onto the screen. Called whenever the screen needs to be redrawn.
    """

    def on_draw(self):
        # print("star_engine on_draw called.")
        pass

    """
    Handles key press events. Called when a key is pressed.
    
    Args:
        symbol (int): The key symbol of the pressed key.
        modifiers (int): Bitwise modifier mask (e.g., shift, ctrl).
    """

    def on_key_press(self, symbol, modifiers):
        print("star_engine on_key_press called.", symbol, modifiers)
        pass

    def run(self):
        # Starts the main game loop and schedules the update method for 60 frames per second.
        # calls the update method 60 times per second
        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

        @self.window.event
        def on_draw():
            self.on_draw()

        @self.window.event
        def on_key_press(symbol, modifiers):
            self.on_key_press(symbol, modifiers)

        pyglet.app.run()
