import pygame

from components.ui.ui_component import UIComponent


class Panel(UIComponent):
    """
    A rectangular panel with optional corner radius and alpha.
    Can serve as a background container for other components.
    """
    def __init__(self, rect, color, corner_radius=0):
        """
        :param rect: A pygame.Rect specifying the position/size of the panel.
        :param color: A tuple (R, G, B, A) or (R, G, B).
        :param corner_radius: Rounded corner radius (default 0 = no rounding).
        """
        self.rect = rect
        self.color = color
        self.corner_radius = corner_radius

    def draw(self, surface):
        """
        Draws the panel onto the given surface. Uses an intermediate
        Surface if color has alpha.
        """
        # Create a temporary surface with alpha channel
        panel_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            self.color,
            panel_surface.get_rect(),
            border_radius=self.corner_radius
        )
        # Blit the panel onto the main surface at rect.x, rect.y
        surface.blit(panel_surface, (self.rect.x, self.rect.y))

    def handle_event(self, event):
        pass