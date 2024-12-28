from src.star_engine import StarEngine

class Game:
    def __init__(self, engine: StarEngine):
        self.engine: StarEngine = engine

    def run(self):
        self.engine.run()