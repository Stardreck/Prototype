# File: ..\main.py
from src.games.story_game import StoryGame
from src.star_engine import StarEngine


def main():
    # init game engine
    engine = StarEngine()
    # init default game
    game = StoryGame(engine)
    # start game loop
    game.run()

# entry point
if __name__ == "__main__":
    main()


# File: ../src\star_config.py
class StarConfig:
    def __init__(self, title: str):
        self.title: str = title

# File: ../src\star_engine.py
import json

import pyglet

from src.scenes.scene import Scene
from src.scenes.story_scene import StoryScene
from src.star_config import StarConfig


class StarEngine:
    def __init__(self):
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


# File: ../src\games\game.py
import pyglet

from src.star_engine import StarEngine


class Game:
    def __init__(self, engine):
        self.engine: StarEngine = engine

    def run(self):
        self.engine.run()
        self.show_menu()

    def show_menu(self):
        pass

# File: ../src\games\story_game.py
from src.games.game import Game
from src.star_engine import StarEngine


class StoryGame(Game):
	def __init__(self, engine: StarEngine):
		super().__init__(engine)



# File: ../src\scenes\scene.py
import pyglet

class Scene:
    def __init__(self, id, game_id, background, text):
        self.id = id
        self.game_id = game_id
        self.background_path = background
        self.text = text
        self.background = None

    def load_assets(self):
        try:
            self.background = pyglet.resource.image(self.background_path)
        except pyglet.resource.ResourceNotFoundException:
            print(f"Background image {self.background_path} not found.")

    def render(self, window):
        if self.background:
            self.background.blit(0, 0)
        label = pyglet.text.Label(
            self.text,
            font_name='Arial',
            font_size=20,
            x=window.width // 2,
            y=window.height // 2,
            width=window.width - 40,
            multiline=True,
            anchor_x='center',
            anchor_y='center'
        )
        label.draw()


# File: ../src\scenes\story_scene.py
from .scene import Scene

class StoryScene(Scene):
    def __init__(self, id, game_id, background, text):
        super().__init__(id, game_id, background, text)

# File: ../src\views\main_view.py
from src.views.view import View


class MainView(View):
    def __init__(self):
        super().__init__()

# File: ../src\views\view.py
class View:
    def render(self):
        pass

