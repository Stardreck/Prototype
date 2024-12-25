import json

import pyglet

from src.scenes.story_scene import StoryScene
from src.star_config import StarConfig


class StarEngine:
    def __init__(self):
        self.config: StarConfig | None = None
        self.load_config_from_json()

        self.window: pyglet.window.Window = pyglet.window.Window(width=800, height=600, caption=self.config.title)
        self.window.push_handlers(self)

       # self.scenes: list[StoryScene] = self.load_scenes_from_json("data/scenes.json")

    def load_config_from_json(self):
        with open("data/config.json", 'r') as file:
            data = json.load(file)
        self.config: StarConfig = StarConfig(data["title"])

    def load_scenes_from_json(self, json_file):
        with open(json_file, 'r') as file:
            data = json.load(file)
        scenes = []
        for scene_data in data:
            scene = StoryScene(
                id=scene_data["id"],
                game_id=scene_data["game_id"],
                background=scene_data["background"],
                text=scene_data["text"]
            )
            scene.load_assets()
            scenes.append(scene)
        return scenes

    def run(self):
        pyglet.app.run()