from src.games.game import Game
from star_engine import StarEngine


class StoryGame(Game):
    def __init__(self, engine: StarEngine):
        super().__init__(engine)
        
    def run(self):
        super().run()
