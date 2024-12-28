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