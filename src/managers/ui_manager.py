import pygame
from typing import List, TYPE_CHECKING

from enums.color import Color

if TYPE_CHECKING:
    from games.story_game import StoryGame


class UIManager:
    """
    Manages UI elements such as HUDs, overlays, and quiz interfaces.
    """

    def __init__(self, game: "StoryGame") -> None:
        """
        Initialize the UIManager with a reference to the game instance.
        """
        self.game: 'StoryGame' = game
        self.font_hud: pygame.font.Font = pygame.font.SysFont(None, 28)
        self.font_overlay: pygame.font.Font = pygame.font.SysFont(None, 24)

    def draw_hud(self, surface: pygame.Surface) -> None:
        """
        Draw the HUD overlay showing fuel and hull.
        """
        hud_line: str = f"Fuel: {self.game.fuel} | Hull: {self.game.hull}"
        surf: pygame.Surface = self.font_hud.render(hud_line, True, Color.WHITE.value)
        surface.blit(surf, (20, 20))

    def display_text_blocking(self, text: str) -> None:
        """
        Display a blocking text overlay that waits for user input to continue.
        """
        waiting: bool = True

        if self.game.debug_manager.debug_mode:
            target_surf: pygame.Surface = self.game.screen.subsurface(self.game.game_rect)
            ow_w: int = self.game.game_rect.width
            ow_h: int = 180
        else:
            target_surf: pygame.Surface = self.game.screen
            ow_w: int = self.game.screen.get_width()
            ow_h: int = 180

        overlay_rect: pygame.Rect = pygame.Rect(0, target_surf.get_height() - ow_h, ow_w, ow_h)
        clock: pygame.time.Clock = pygame.time.Clock()

        while waiting and self.game.is_running:
            dt: int = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        waiting = False
                    elif event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                    elif event.key == pygame.K_ESCAPE:
                        self.game.stop()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            self.game.draw()

            text_overlay: pygame.Surface = pygame.Surface((ow_w, ow_h))
            text_overlay.set_alpha(180)
            text_overlay.fill(Color.BLACK.value)

            lines: List[str] = self.wrap_text(text, self.font_overlay, ow_w - 20)
            y_off: int = 10
            for line in lines:
                line_img: pygame.Surface = self.font_overlay.render(line, True, Color.WHITE.value)
                text_overlay.blit(line_img, (10, y_off))
                y_off += line_img.get_height() + 5

            target_surf.blit(text_overlay, (overlay_rect.x, overlay_rect.y))
            pygame.display.flip()

    @staticmethod
    def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """
        Helper method to wrap text into multiple lines based on max width.
        """
        words: List[str] = text.split(" ")
        lines: List[str] = []
        current_line: str = ""
        for w in words:
            test_line: str = current_line + w + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = w + " "
        if current_line:
            lines.append(current_line.strip())
        return lines
