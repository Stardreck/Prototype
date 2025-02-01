import pygame
from components.ui.ui_component import UIComponent

class MultiLineText(UIComponent):
    """
    A UI component that displays text that wraps into multiple lines
    if it exceeds a specified maximum width.
    """
    def __init__(self, text: str, font: pygame.font.Font, color: tuple, position: tuple[int, int], max_width: int, line_spacing: int = 5):
        """
        :param text: The text to be displayed.
        :param font: A pygame.font.Font object.
        :param color: Text color as an RGB tuple.
        :param position: Tuple (x, y) for the starting position (position of the first line).
        :param max_width: Maximum width that a line should not exceed.
        :param line_spacing: Additional spacing (in pixels) between lines.
        """
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.max_width = max_width
        self.line_spacing = line_spacing

        # Compute the wrapped text
        self.lines = self._wrap_text()

    def _wrap_text(self) -> list[str]:
        """
        Splits the text into lines so that each line does not exceed max_width in pixels.
        """
        words = self.text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            # Construct a test line: if current_line is empty, use the word; otherwise, append with a space
            test_line = word if current_line == "" else current_line + " " + word
            # Check if the test line fits within max_width
            if self.font.size(test_line)[0] <= self.max_width:
                current_line = test_line
            else:
                # If current_line already has content, add it to the list
                if current_line:
                    lines.append(current_line)
                # Start a new line with the current word
                current_line = word
        # Add the last line
        if current_line:
            lines.append(current_line)
        return lines

    def set_text(self, text: str):
        """
        Updates the displayed text and recalculates the line wrapping.
        """
        self.text = text
        self.lines = self._wrap_text()

    def draw(self, surface: pygame.Surface):
        """
        Draws the wrapped text onto the given surface.
        """
        x, y = self.position
        for line in self.lines:
            text_surf = self.font.render(line, True, self.color)
            surface.blit(text_surf, (x, y))
            # Increase y by the height of the line plus additional line spacing
            y += self.font.get_linesize() + self.line_spacing

    def handle_event(self, event):
        pass
