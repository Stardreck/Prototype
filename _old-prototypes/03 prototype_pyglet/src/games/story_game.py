from src.games.game import Game
from src.star_engine import StarEngine


class StoryGame(Game):
	def __init__(self, engine: StarEngine):
		super().__init__(engine)

