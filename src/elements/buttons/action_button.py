import pygame

from enums.color import Color


class ActionButton:
    def __init__(self, rect: pygame.Rect, text: str, font: pygame.font.Font,
                 bg_color: tuple, text_color: tuple):
        self.rect = rect
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover = False

        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg_color, self.rect)
        if self.hover:
            pygame.draw.rect(surface, Color.BUTTON_HOVER.value, self.rect, 3)
        else:
            pygame.draw.rect(surface, Color.BUTTON_BG.value, self.rect, 3)
        surface.blit(self.text_surf, self.text_rect)

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)