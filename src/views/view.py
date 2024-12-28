from pygame import Surface


class View:
    def __init__(self, screen: Surface):
        self.screen: Surface = screen

    def render(self):
        pass