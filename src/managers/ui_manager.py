from __future__ import annotations

import pygame
from typing import List, TYPE_CHECKING, Optional, cast

from components.ui.buttons.action_button import ActionButton
from components.ui.buttons.button import Button
from components.ui.image import Image
from components.ui.multiline_text import MultiLineText
from components.ui.panel import Panel
from components.ui.text import Text
from components.ui.ui_component import UIComponent
from enums.color import Color
from managers.hud_manager import HUDManager
from plugins.video_player import VideoPlayer

if TYPE_CHECKING:
    from games.story_game import StoryGame


class UIManager:
    """
    Manages UI elements such as HUDs, overlays, and quiz interfaces.
    """

    def __init__(self, game: StoryGame) -> None:
        """
        Initialize the UIManager with a reference to the game instance.
        """
        self.game: StoryGame = game
        self.font_hud: pygame.font.Font = pygame.font.SysFont(None, 28)
        self.font_overlay: pygame.font.Font = pygame.font.SysFont(None, 24)
        self.font_button: pygame.font.Font = pygame.font.SysFont(None, 32)

        ##### HUD #####
        self.hud = HUDManager(game)

        ##### init UI components #####
        # default panel
        self.default_panel_bg = Panel(
            pygame.Rect(528, 123, 545, 473),
            (16, 26, 23, 230),  # with alpha
            corner_radius=12
        )
        self.default_panel = Panel(
            pygame.Rect(538, 130, 525, 399),
            (10, 17, 15),  # no alpha
            corner_radius=12
        )
        self.default_panel_title = Text("",
                                        self.font_overlay,
                                        (255, 255, 255),
                                        (538 + 221, 130 + 15))

        self.default_panel_subtitle = MultiLineText(
            text="",
            font=self.font_overlay,
            color=(255, 255, 255),
            position=(538 + 20, 130 + 70),
            max_width=492,
            line_spacing=5
        )
        self.default_panel_confirm_button = Button(
            rect=pygame.Rect(self.default_panel_bg.rect.centerx - 262,
                             self.default_panel_bg.rect.bottom - 50,
                             525,
                             39),
            color=(23, 78, 56),
            hover_color=(24, 39, 33),
            corner_radius=12,
            text="Bestätigen",
            font=self.font_button,
            text_color=(255, 255, 255)
        )
        # choice panel (with image, text and 2 buttons
        self.choice_panel_bg = Panel(
            pygame.Rect(528, 123, 545, 473),
            (16, 26, 23, 230),  # with alpha
            corner_radius=12
        )
        self.choice_panel = Panel(
            pygame.Rect(538, 130, 525, 333),
            (10, 17, 15),  # no alpha
            corner_radius=12
        )
        self.choice_panel_imge = Image(
            image_path="",
            position=(549, 169),
            width=241,
            height=257
        )
        self.choice_panel_title = Text(
            text="",
            font=self.font_overlay,
            color=(255, 255, 255),
            position=(800, 169)
        )
        self.choice_panel_description = MultiLineText(
            text="",
            font=self.font_overlay,
            color=(255, 255, 255),
            position=(800, 229),
            max_width=246,
            line_spacing=5
        )

        self.choice_panel_second_button = Button(
            rect=pygame.Rect(self.default_panel_bg.rect.centerx - 262,
                             self.default_panel_bg.rect.bottom - 50,
                             525,
                             39),
            color=(23, 78, 56),
            hover_color=(24, 39, 33),
            corner_radius=12,
            text="",
            font=self.font_button,
            text_color=(255, 255, 255)
        )
        self.choice_panel_first_button = Button(
            rect=pygame.Rect(self.choice_panel_second_button.rect.left,
                             self.choice_panel_second_button.rect.top - 60,
                             525,
                             39),
            color=(23, 78, 56),
            hover_color=(24, 39, 33),
            corner_radius=12,
            text="",
            font=self.font_button,
            text_color=(255, 255, 255)
        )


        self.ui_components: dict[str, UIComponent] = {
            "default_panel_bg": self.default_panel_bg,
            "default_panel": self.default_panel,
            "default_panel_title": self.default_panel_title,
            "default_panel_subtitle": self.default_panel_subtitle,
            "default_panel_confirm_button": self.default_panel_confirm_button,
            "choice_panel_bg": self.choice_panel_bg,
            "choice_panel": self.choice_panel,
            "choice_panel_second_button": self.choice_panel_second_button,
            "choice_panel_first_button": self.choice_panel_first_button,
            "choice_panel_title": self.choice_panel_title,
            "choice_panel_description": self.choice_panel_description,
            "choice_panel_image": self.choice_panel_imge,
        }

    def draw_hud(self, surface: pygame.Surface) -> None:
        """
        Draw the HUD overlay showing fuel and hull.
        """
        self.hud.draw(surface)

    def display_message_overlay(self, message: str) -> None:
        """
        Displays an overlay message with a single confirm button ("Bestätigen").
        When the confirm button is clicked, the overlay is dismissed.
        """
        # Set the overlay message on the default panel subtitle.
        subtitle = cast(MultiLineText, self.ui_components.get("default_panel_subtitle"))
        subtitle.set_text(message)

        # Create a temporary confirm button with the same style as the default one.
        default_confirm = cast(Button, self.ui_components.get("default_panel_confirm_button"))
        temp_confirm_button = Button(
            rect=default_confirm.rect,
            color=default_confirm.color,
            hover_color=default_confirm.hover_color,
            corner_radius=default_confirm.corner_radius,
            text="Bestätigen",
            font=default_confirm.font,
            text_color=default_confirm.text_color
        )

        # A flag to know when the button has been pressed.
        confirmed = [False]

        # Define the callback that sets the confirmation flag.
        def on_confirm():
            print("Confirm button pressed!")
            confirmed[0] = True

        temp_confirm_button.set_on_click(on_confirm)

        # Run the overlay loop until the confirm button is pressed.
        while not confirmed[0] and self.game.is_running:
            # Process events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return
                temp_confirm_button.handle_event(event)
            # Draw the overlay using the default panel background and panel.
            target_surface = self.game.screen
            self.ui_components["default_panel_bg"].draw(target_surface)
            self.ui_components["default_panel"].draw(target_surface)
            subtitle.draw(target_surface)
            temp_confirm_button.draw(target_surface)
            pygame.display.flip()
            pygame.time.delay(50)

        temp_confirm_button.set_on_click(None)

        # Once confirmed, exit the loop (temp_confirm_button will be garbage-collected).

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

        buttons: List[ActionButton] = []

        for idx, option in enumerate(options):
            button_x = (overlay_width - button_width) // 2
            button_y = start_y + idx * (button_height + button_spacing)
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            button = ActionButton(
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
