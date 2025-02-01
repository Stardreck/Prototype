from __future__ import annotations
import pygame

from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from games.story_game import StoryGame



class InputManager:
    """
    Handles user input and delegates actions to the game logic.
    """
    def __init__(self, game: StoryGame):
        """
        Initializes the InputManager with a reference to the game instance.
        :param game: The game instance that will receive input events.
        """
        self.game = game

    def process_events(self):
        """
        Processes all incoming events and triggers corresponding game actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.stop()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.handle_mouse_button_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_button_up(event)
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event)

            for key, component in self.game.ui_manager.ui_components.items():
                component.handle_event(event)


    def handle_keydown(self, event: pygame.event.Event):
        """
        Handles keydown events and triggers game-specific actions.
        :param event: The pygame.KEYDOWN event.
        """
        if event.key == pygame.K_ESCAPE:
            self.game.stop()
        elif event.key == pygame.K_d:
            self.game.debug_manager.toggle_debug_mode()

        else:
            self.game.handle_movement(event)
        #
        # elif event.key == pygame.K_UP:
        #     self.game.move_player(-1, 0)
        # elif event.key == pygame.K_DOWN:
        #     self.game.move_player(1, 0)
        # elif event.key == pygame.K_LEFT:
        #     self.game.move_player(0, -1)
        # elif event.key == pygame.K_RIGHT:
        #     self.game.move_player(0, 1)

    def handle_mouse_button_down(self, event: pygame.event.Event):
        self.game.handle_touch_mouse_down(event)

    def handle_mouse_button_up(self,  event: pygame.event.Event):
        self.game.handle_touch_mouse_up(event)

    def handle_mouse_motion(self,  event: pygame.event.Event):
        self.game.handle_touch_mouse_motion(event)