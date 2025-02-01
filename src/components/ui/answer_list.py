from components.ui.ui_component import UIComponent


class AnswerList(UIComponent):
    """
    A component that displays multiple answers (strings) in a vertical list.
    """
    def __init__(self, answers, font, color, start_position, line_spacing=40):
        """
        :param answers: A list of strings to display as answers.
        :param font: A pygame.font.Font or SysFont object.
        :param color: Text color (R, G, B).
        :param start_position: Top-left position as a tuple (x, y).
        :param line_spacing: Vertical distance between each line of text.
        """
        self.answers = answers
        self.font = font
        self.color = color
        self.start_position = start_position
        self.line_spacing = line_spacing

    def set_answers(self, answers):
        self.answers = answers

    def draw(self, surface):
        """
        Renders each string in `answers` in a vertical list.
        """
        x, y = self.start_position
        index = 1
        for answer in self.answers:
            text_surf = self.font.render(f"[{index}]         {answer}", True, self.color)
            surface.blit(text_surf, (x, y))
            y += self.line_spacing
            index += 1

    def handle_event(self, event):
        pass