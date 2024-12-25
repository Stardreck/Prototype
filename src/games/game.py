import pyglet

from src.star_engine import StarEngine


class Game:
    def __init__(self, engine):
        self.engine: StarEngine = engine;