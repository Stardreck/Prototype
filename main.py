import pyglet
from pyglet.window import key
import json

from src.scenes.story_scene import StoryScene


def load_scenes_from_json(json_file):
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

def main():
    print("Hello World!")
    scenes = load_scenes_from_json("data/scenes.json")
    print(scenes)

if __name__ == "__main__":
    main()




