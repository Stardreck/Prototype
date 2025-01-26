from __future__ import annotations

import random
import pygame

from typing import List, TYPE_CHECKING
from enums.color import Color
from managers.event_selection_manager import EventSelectionManager
from models.event_card import EventCard

if TYPE_CHECKING:
    from games.story_game import StoryGame


class EventManager:
    def __init__(self, game: StoryGame, event_cards: List[EventCard], base_probability: float = 0.3):
        self.game = game
        self.negative_events: List[EventCard] = [card for card in event_cards if card.type == "negative"]
        self.positive_events: List[EventCard] = [card for card in event_cards if card.type == "positive"]
        self.ui_manager = self.game.ui_manager
        self.error_count: int = 0
        self.max_error: int = 5
        self.event_probability: float = base_probability

        self.selection_manager = EventSelectionManager(self.game, self.negative_events, self.positive_events, base_probability, self.max_error)

        ##### load event card backgrounds #####
        self.event_card_surfaces = {}
        self.__load_event_assets()

    def increase_error_count(self):
        """Increase the error count, up to the maximum limit."""
        if self.error_count < self.max_error:
            self.error_count += 1
        self.selection_manager.set_error_count(self.error_count)

    def decrease_error_count(self):
        """Decrease the error count, down to zero."""
        if self.error_count > 0:
            self.error_count -= 1
        self.selection_manager.set_error_count(self.error_count)

    def trigger_random_event(self):
        """
        Check if an event should be triggered and handle it.
        """
        card = self.selection_manager.pick_event()
        if card:
            self.selection_manager.apply_event_scaling(card)
            self.display_event_card_animated(card)
            self.apply_event_effects(card)

    def should_trigger_event(self) -> bool:
        """Determine if an event should be triggered."""
        return self.selection_manager.should_trigger_event()


    def apply_event_effects(self, event_card: EventCard) -> None:
        """
        Apply the effects of the event to the game state.

        :param event_card: The EventCard whose effects to apply.
        """
        event_card.apply_effect(self.game)

        # Check for game over condition
        if self.game.hull <= 0:
            self.game.game_over("Hull <= 0. Ship destroyed!")

    def display_event_card_animated(self, card: EventCard) -> None:
        """
        Display an animated event card with its description.
        """
        waiting: bool = True
        clock: pygame.time.Clock = pygame.time.Clock()
        start_time: int = pygame.time.get_ticks()
        duration: int = 1000  # milliseconds

        # Load the event card surface
        card_surface: pygame.Surface = self.__get_card_surface(card.name)
        if not card_surface:
            # Fallback if image not found
            card_surface = pygame.Surface((200, 300))
            card_surface.fill((150, 0, 150))

        # Scale the card surface
        target_w: int = 200
        ratio: float = card_surface.get_width() / card_surface.get_height()
        target_h: int = int(target_w / ratio)
        card_surface = pygame.transform.smoothscale(card_surface, (target_w, target_h))

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
        font_overlay: pygame.font.Font = pygame.font.SysFont(None, 24)
        text_lines: List[str] = self.game.ui_manager.wrap_text(card.description, font_overlay, sw - 20)

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
            rot_surf: pygame.Surface = pygame.transform.rotate(card_surface, angle)
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
                line_img: pygame.Surface = font_overlay.render(line, True, Color.WHITE.value)
                text_overlay.blit(line_img, (10, y_offset))
                y_offset += line_img.get_height() + 5

            target_surf.blit(text_overlay, (0, y_pos + rh + 10))
            pygame.display.flip()

            # If animation is done and user hasn't clicked, wait for click
            if not anim_running:
                continue

    def __calculate_event_probability(self) -> float:
        """Calculate the probability of triggering an event based on error count."""
        return self.event_probability + (0.05 * self.error_count)

    def __get_card_surface(self, card_name: str) -> pygame.Surface | None:
        return self.event_card_surfaces.get(card_name, None)

    def __load_event_assets(self):
        """

        """
        for card in self.negative_events + self.positive_events:
            try:
                surf = pygame.image.load(card.image).convert_alpha()
            except:
                surf = pygame.Surface((200, 300))
                surf.fill((150, 0, 150))
            self.event_card_surfaces[card.name] = surf
