from .scene import Scene

class StoryScene(Scene):
    def __init__(self, id, game_id, background, text):
        super().__init__(id, game_id, background, text)