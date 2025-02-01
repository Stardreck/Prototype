from components.ui.ui_component import UIComponent


class Text(UIComponent):
    """
    A simple text component that renders one line of text at a given position.
    """
    def __init__(self, text, font, color, position):
        """
        :param text: The string to be rendered.
        :param font: A pygame.font.Font or SysFont object.
        :param color: The text color (R, G, B).
        :param position: A tuple (x, y) for the top-left position.
        """
        self.text = text
        self.font = font
        self.color = color
        self.position = position

    def set_text(self, text):
        self.text = text

    def draw(self, surface):
        """
        Renders the text onto the surface at the specified position.
        """
        text_surf = self.font.render(self.text, True, self.color)
        surface.blit(text_surf, self.position)


    def handle_event(self, event):
        pass