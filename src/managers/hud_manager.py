from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

from enums.button_state import ButtonState
from enums.color import Color

if TYPE_CHECKING:
    from games.story_game import StoryGame


class HUDManager:
    def __init__(self, game: StoryGame):
        self.game: StoryGame = game
        self.__init_hud()
        self.font: pygame.font.Font = pygame.font.SysFont(None, 28)

    def __init_hud(self):
        hud_size = 50
        icon_size = 40
        ##### topbar #####
        self.topbar_background = pygame.image.load("assets/interface/hud/topbar_background.png")
        self.topbar_background = pygame.transform.scale(self.topbar_background,
                                                        (self.game.screen.get_width(), hud_size))
        ##### topbar ressource icons #####
        self.fuel_icon = pygame.image.load("assets/icons/fuel_icon.png")
        self.fuel_icon = pygame.transform.scale(self.fuel_icon, (icon_size, icon_size))

        ##### sidebar #####
        self.sidebar_background = pygame.image.load("assets/interface/hud/sidebar_background.png")
        self.sidebar_background = pygame.transform.scale(self.sidebar_background,
                                                         (hud_size, self.game.screen.get_height()))
        ##### sidebar elements #####
        self.inventory_button_image = pygame.image.load("assets/artifact.png")
        self.inventory_button_image = pygame.transform.scale(self.inventory_button_image, (icon_size, icon_size))
        self.inventory_button_rect = self.inventory_button_image.get_rect(topleft=(5, 80))
        ##### inventory #####
        window_inventory_width = self.game.screen.get_width() - 400
        window_inventory_height = self.game.screen.get_height() - 200
        self.inventory_background = pygame.image.load("assets/interface/relics_panel_bg.png")
        self.inventory_background = pygame.transform.scale(self.inventory_background,
                                                           (window_inventory_width, window_inventory_height))
        self.inventory_background_rect = pygame.Rect(200, 100, window_inventory_width, window_inventory_height)
        ##### element close button #####
        # Load close button and split into states
        self.close_button_image = pygame.image.load("assets/close_button.png")
        self.close_button_width, self.close_button_height = self.close_button_image.get_size()
        self.close_button_state_width = self.close_button_width // 3
        self.close_button_rect = pygame.Rect(self.game.screen.get_width() - 240, 120, self.close_button_state_width,
                                             self.close_button_height)
        ##### inventory objects #####
        self.inventory_empty_slot = pygame.image.load("assets/interface/inventory/inventory_empty_place.png")
        self.inventory_empty_slot = pygame.transform.scale(self.inventory_empty_slot, (100, 100))

        ##### corner #####
        self.corner_decoration = pygame.image.load("assets/interface/hud/corner_decoration.png")
        self.corner_decoration = pygame.transform.scale(self.corner_decoration, (66, 76))

    def __draw_top_bar(self, surface: pygame.Surface):
        ##### topbar background #####
        surface.blit(self.topbar_background, (0, 0))
        ##### fuel ressource #####
        self.game.screen.blit(self.fuel_icon, (80, 5))
        fuel_text = self.font.render(f"{self.game.fuel}", True, Color.WHITE.value)
        self.game.screen.blit(fuel_text, (130, 15))
        ##### hull ressource #####
        self.game.screen.blit(self.fuel_icon, (210, 5))
        hull_text = self.font.render(f"{self.game.hull}", True, Color.WHITE.value)
        self.game.screen.blit(hull_text, (260, 15))

    def __draw_sidebar(self, surface: pygame.Surface):
        ##### sidebar background #####
        self.game.screen.blit(self.sidebar_background, (0, 50))
        ##### sidebar elements #####
        self.game.screen.blit(self.inventory_button_image, self.inventory_button_rect)

    def __draw_corner(self, surface: pygame.Surface):
        self.game.screen.blit(self.corner_decoration, (0, 0))

    def draw(self, surface: pygame.Surface):
        """
        Draw the HUD overlay showing fuel and hull.
        """
        self.__draw_top_bar(surface)
        self.__draw_sidebar(surface)
        self.__draw_corner(surface)

        if self.game.is_inventory_open:
            self.draw_inventory(surface)

    def draw_inventory(self, surface: pygame.Surface):
        ##### background #####
        self.game.screen.blit(self.inventory_background, self.inventory_background_rect.topleft)
        ##### title #####
        title_text = self.font.render(f"Inventory", True, Color.WHITE.value)
        self.game.screen.blit(title_text, (self.game.screen.get_width() // 2 - 70, 110))
        ##### close button #####
        close_button_image_state = self.close_button_image.subsurface(
            self.game.sidebar_close_button_state.value * self.close_button_state_width, 0,
            self.close_button_state_width,
            self.close_button_height
        )
        self.game.screen.blit(close_button_image_state, self.close_button_rect.topleft)

        ##### draw game objects #####
        self.__draw_inventory_objects()

    def __draw_inventory_objects(self):
        # Center inventory grid
        slot_width, slot_height = 100, 100
        grid_rows, grid_cols = 2, 4
        slot_spacing = 120

        grid_width = grid_cols * slot_width + (grid_cols - 1) * (slot_spacing - slot_width)
        grid_height = grid_rows * slot_height + (grid_rows - 1) * (slot_spacing - slot_height)

        # coordinates for the first object
        start_x = self.inventory_background_rect.left + (self.inventory_background_rect.width - grid_width) // 2
        start_y = self.inventory_background_rect.top + (self.inventory_background_rect.height - grid_height) // 2

        # get inventory objects, clone the list otherwise it would override it (call by reference)
        objects = self.game.inventory_manager.get_items().copy()

        # Draw inventory grid
        for row in range(grid_rows):  # 2 rows
            for col in range(grid_cols):  # 4 columns
                x_pos = start_x + col * slot_spacing
                y_pos = start_y + row * slot_spacing
                if len(objects) != 0:
                    inventory_active_slot = pygame.image.load(objects[0].image_path)
                    inventory_active_slot = pygame.transform.scale(inventory_active_slot, (100, 100))
                    self.game.screen.blit(inventory_active_slot, (x_pos, y_pos))
                    objects.pop(0)
                else:
                    self.game.screen.blit(self.inventory_empty_slot, (x_pos, y_pos))
