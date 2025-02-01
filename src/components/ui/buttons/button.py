import pygame

from components.ui.ui_component import UIComponent


class Button(UIComponent):
    """
    A clickable button with hover-state detection and optional text.
    """
    def __init__(self, rect, color, hover_color, corner_radius=0, text=None, font=None, text_color=(255,255,255)):
        """
        :param rect: A pygame.Rect specifying button position/size.
        :param color: Normal color (R, G, B).
        :param hover_color: Color used when the mouse is over the button (R, G, B).
        :param corner_radius: Rounded corner radius.
        :param text: Text to be displayed on the button (optional).
        :param font: A pygame.font.Font or SysFont object (optional).
        :param text_color: Color for the text (R, G, B).
        """
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.corner_radius = corner_radius
        self.text = text
        self.font = font
        self.text_color = text_color

        # Callback function if needed (on_click)
        self.on_click_callback = None

    def set_on_click(self, callback):
        """
        Assign a function that should be called when the button is clicked.
        """
        self.on_click_callback = callback

    def set_text(self, text):
        self.text = text

    def draw(self, surface):
        """
        Draw the button (choosing hover or normal color) and optional text.
        """
        # Detect hover
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        fill_color = self.hover_color if is_hovered else self.color

        # Draw the button background
        pygame.draw.rect(
            surface,
            fill_color,
            self.rect,
            border_radius=self.corner_radius
        )

        # If there is text, draw it centered in the button
        if self.text and self.font:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        """
        Handle mouse click events. If the button is clicked and
        on_click_callback is set, call it.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                print("[Button] clicked!", self.on_click_callback)
            if self.rect.collidepoint(mouse_pos) and self.on_click_callback:
                self.on_click_callback()