import pyglet
from kivy.app import App

from src.star_engine import StarEngine
from src.views.view import View


class Game(App):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine: StarEngine = engine

    def build(self):
        return self.engine.screen_manager

    def run(self):
        self.engine.run()
        self.engine.add_screen(View(name="intro"))
        self.engine.set_screen("intro")

        # start kivy event loop
        super().run()

    def show_menu(self):
        pass