import pygame
from typing import List

from enums.color import Color
from models.event_card import EventCard


class UIManager:
    """
    Manages UI elements such as HUDs, overlays, and quiz interfaces.
    """

    def __init__(self, game: 'StoryGame') -> None:
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

    def display_event_card_animated(self, card: EventCard) -> None:
        """
        Display an animated event card with its description.
        """
        waiting: bool = True
        clock: pygame.time.Clock = pygame.time.Clock()
        start_time: int = pygame.time.get_ticks()
        duration: int = 1000  # milliseconds

        # Load the event card surface
        card_surf: pygame.Surface = self.game.event_manager.get_card_surface(card.name)
        if not card_surf:
            # Fallback if image not found
            card_surf = pygame.Surface((200, 300))
            card_surf.fill((150, 0, 150))

        # Scale the card surface
        target_w: int = 200
        ratio: float = card_surf.get_width() / card_surf.get_height()
        target_h: int = int(target_w / ratio)
        card_surf = pygame.transform.smoothscale(card_surf, (target_w, target_h))

        # Determine center position
        target_surf: pygame.Surface = (
            self.game.screen.subsurface(self.game.game_rect)
            if self.game.debug_manager.debug_mode
            else self.game.screen
        )
        sw: int = target_surf.get_width()
        sh: int = target_surf.get_height()
        center_x: int = sw // 2
        center_y: int = sh // 2

        # Prepare text
        text_lines: List[str] = self.wrap_text(card.description, self.font_overlay, sw - 20)

        anim_running: bool = True
        angle: float = 0.0

        while waiting and self.game.is_running:
            dt: int = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.stop()
                        return
                    elif event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # User clicked to skip animation
                    waiting = False
                    break

            self.game.draw()  # Draw background and other elements

            elapsed: int = pygame.time.get_ticks() - start_time
            frac: float = elapsed / duration
            if frac >= 1.0:
                frac = 1.0
                anim_running = False

            # Calculate current position and rotation
            current_y: float = center_y + 200 * (1 - frac)
            angle: float = 360.0 * frac

            # Rotate the card surface
            rot_surf: pygame.Surface = pygame.transform.rotate(card_surf, angle)
            rw: int = rot_surf.get_width()
            rh: int = rot_surf.get_height()

            # Position the rotated surface
            x_pos: int = (sw - rw) // 2
            y_pos: int = int(current_y - rh / 2)

            # Blit the rotated card
            target_surf.blit(rot_surf, (x_pos, y_pos))

            # Draw description text below the card
            text_overlay: pygame.Surface = pygame.Surface((sw, 100))
            text_overlay.set_alpha(180)
            text_overlay.fill(Color.BLACK.value)

            y_offset: int = 10
            for line in text_lines:
                line_img: pygame.Surface = self.font_overlay.render(line, True, Color.WHITE.value)
                text_overlay.blit(line_img, (10, y_offset))
                y_offset += line_img.get_height() + 5

            target_surf.blit(text_overlay, (0, y_pos + rh + 10))
            pygame.display.flip()

            # If animation is done and user hasn't clicked, wait for click
            if not anim_running:
                continue

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
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
