# src/managers/ui_manager.py

import pygame
from typing import List, TYPE_CHECKING, Optional

from enums.color import Color
from plugins.video_player import VideoPlayer

if TYPE_CHECKING:
    from games.story_game import StoryGame


class UIManager:
    """
    Manages UI elements such as HUDs, overlays, and quiz interfaces.
    """

    class Button:
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

    def __init__(self, game: "StoryGame") -> None:
        """
        Initialize the UIManager with a reference to the game instance.
        """
        self.game: 'StoryGame' = game
        self.font_hud: pygame.font.Font = pygame.font.SysFont(None, 28)
        self.font_overlay: pygame.font.Font = pygame.font.SysFont(None, 24)
        self.font_button: pygame.font.Font = pygame.font.SysFont(None, 32)  # Neue Font für Buttons

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

    def display_multiple_choice(self, prompt: str, options: List[str]) -> Optional[int]:
        """
        Display multiple-choice buttons and return the selected option index.
        :param prompt: The question or prompt to display.
        :param options: A list of option strings.
        :return: The index of the selected option or None if no selection.
        """
        waiting = True
        selected_option = None
        clock = pygame.time.Clock()

        if self.game.debug_manager.debug_mode:
            target_surf: pygame.Surface = self.game.screen.subsurface(self.game.game_rect)
            ow_w: int = self.game.game_rect.width
            ow_h: int = self.game.game_rect.height
        else:
            target_surf: pygame.Surface = self.game.screen
            ow_w: int = self.game.screen.get_width()
            ow_h: int = self.game.screen.get_height()

        # Define the overlay size and position
        overlay_width = int(ow_w * 0.8)
        overlay_height = int(ow_h * 0.6)
        overlay_x = (ow_w - overlay_width) // 2
        overlay_y = (ow_h - overlay_height) // 2

        overlay_rect = pygame.Rect(overlay_x, overlay_y, overlay_width, overlay_height)

        # Create the overlay surface
        overlay_surface = pygame.Surface((overlay_width, overlay_height))
        overlay_surface.set_alpha(220)
        overlay_surface.fill(Color.BLACK.value)

        # Render the prompt
        font = self.font_overlay
        prompt_surf = font.render(prompt, True, Color.WHITE.value)
        prompt_rect = prompt_surf.get_rect(center=(overlay_width // 2, 40))
        overlay_surface.blit(prompt_surf, prompt_rect)

        # Calculate button sizes and positions
        button_width = int(overlay_width * 0.6)
        button_height = 50
        button_spacing = 20
        total_button_height = len(options) * (button_height + button_spacing) - button_spacing
        start_y = (overlay_height - total_button_height) // 2 + 60  # 60 pixels offset for the prompt

        buttons: List[UIManager.Button] = []

        for idx, option in enumerate(options):
            button_x = (overlay_width - button_width) // 2
            button_y = start_y + idx * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button = UIManager.Button(
                rect=button_rect,
                text=option,
                font=self.font_button,
                bg_color=Color.BUTTON_BG.value,
                text_color=Color.WHITE.value
            )
            buttons.append(button)

        while waiting and self.game.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return None
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.stop()
                        return None
                    elif event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Adjust mouse_pos to the target_surf if in debug_mode
                    if self.game.debug_manager.debug_mode:
                        mouse_pos = (mouse_pos[0] - self.game.game_rect.x, mouse_pos[1] - self.game.game_rect.y)
                    if overlay_rect.collidepoint(mouse_pos):
                        relative_pos = (mouse_pos[0] - overlay_x, mouse_pos[1] - overlay_y)
                        for idx, button in enumerate(buttons):
                            if button.rect.collidepoint(relative_pos):
                                selected_option = idx
                                waiting = False
                                break

            # Handle hover states
            mouse_pos = pygame.mouse.get_pos()
            if self.game.debug_manager.debug_mode:
                relative_mouse_pos = (mouse_pos[0] - self.game.game_rect.x, mouse_pos[1] - self.game.game_rect.y)
            else:
                relative_mouse_pos = mouse_pos

            if overlay_rect.collidepoint(relative_mouse_pos):
                relative_pos = (relative_mouse_pos[0] - overlay_x, relative_mouse_pos[1] - overlay_y)
                for button in buttons:
                    if button.rect.collidepoint(relative_pos):
                        button.hover = True
                    else:
                        button.hover = False
            else:
                for button in buttons:
                    button.hover = False

            # Render the UI
            self.game.draw()

            # Draw the overlay
            target_surf.blit(overlay_surface, (overlay_x, overlay_y))

            # Draw buttons on the overlay
            for button in buttons:
                button.draw(overlay_surface)

            pygame.display.flip()
            clock.tick(60)

        return selected_option

    def display_cutscene(self, media_path: str) -> None:
        """
        Display a cutscene image or video and wait for user input to continue.
        :param media_path: Path to the cutscene media (image or video).
        """
        if media_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            # Es ist ein Video, VideoPlayer verwenden
            player = VideoPlayer(self.game.screen)
            player.set_video(media_path)
            player.play()
        else:
            # Angenommen, es ist ein Bild
            waiting = True
            clock = pygame.time.Clock()

            try:
                image = pygame.image.load(media_path).convert()
                image = pygame.transform.scale(image, self.game.screen.get_size())
            except Exception as e:
                print(f"Fehler beim Laden des Cutscene-Bildes {media_path}: {e}")
                image = pygame.Surface(self.game.screen.get_size())
                image.fill(Color.BLACK.value)

            # Optional: Anzeige einer Nachricht
            message = "Klicken Sie oder drücken Sie eine Taste, um fortzufahren"
            font = self.font_overlay
            message_surf = font.render(message, True, Color.WHITE.value)
            message_rect = message_surf.get_rect(
                center=(self.game.screen.get_width() // 2, self.game.screen.get_height() - 50))

            while waiting and self.game.is_running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.game.stop()
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.game.stop()
                            return
                        else:
                            waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False

                # Render das Cutscene-Bild
                self.game.draw()
                self.game.screen.blit(image, (0, 0))
                self.game.screen.blit(message_surf, message_rect)
                pygame.display.flip()
                clock.tick(60)


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
