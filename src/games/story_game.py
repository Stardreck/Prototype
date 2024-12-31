from scenes.story_scene import StoryScene
from src.games.game import Game
from star_engine import StarEngine


class StoryGame(Game):
    def __init__(self, engine: StarEngine):
        super().__init__(engine)
        
    def run(self):
        super().run()
        scene = StoryScene(self.engine.screen, self.engine.view_manager)
        print("scene")
        scene.render()

