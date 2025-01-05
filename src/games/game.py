from enum import Enum

import pygame

from managers.debug_manager import DebugManager
from src.star_engine import StarEngine
class MapState(Enum):
    SYSTEM=1
    SHIP=2

class Game:
    def __init__(self, engine: StarEngine):
        # engine
        self.engine: StarEngine = engine

        # window screen
        self.screen = self.engine.screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
        # surfaces
        self.board_surface = None
        self.overlay_surface = None

        # overlay backgrounds
        self.overlay_background = None

        # todo remove debugger in prod
        self.debug_manager: DebugManager = DebugManager(self.engine.screen)
        self.debug_manager.toggle_debug_mode()
        self.debug_manager.create_surfaces(self)

        # global game states
        self.is_running = True
        self.map_state: MapState = MapState.SYSTEM


    def on_key_press(self, event):
        pass

    def on_quit(self):
        self.is_running = False

    def handle_events(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def run(self):
        # start main loop
        self.engine.run(self)
