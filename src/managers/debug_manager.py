from __future__ import annotations
import math
import pygame
from typing import TYPE_CHECKING, List
from enums.color import Color

if TYPE_CHECKING:
    from games.story_game import StoryGame


class DebugManager:
    def __init__(self):
        self.debug_mode = False

        ##### hexagon grid settings #####
        self.hex_rows = 11
        self.hex_cols = 11
        self.hex_radius = 25
        self.offset_x = 150
        self.offset_y = 200

        self.font = pygame.font.SysFont(None, 24)

        # solar system background image
        self.bg_solar_system = None
        self.load_solar_system_image()

    def load_solar_system_image(self):
        try:
            self.bg_solar_system = pygame.image.load("assets/Sonnensystem38x38.png").convert()
        except:
            self.bg_solar_system = pygame.Surface((500, 500))
            self.bg_solar_system.fill((0, 0, 0))

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        print(f"[DEBUG] Modus: {self.debug_mode}")

    def draw_debug(self, surface: pygame.Surface, game: StoryGame):
        if not self.debug_mode:
            surface.fill(Color.DEBUG_BG.value)
            return

        surface.fill(Color.BLACK.value)
        self.__draw_sonnensystem_bg(surface)
        self.__draw_hex_grid(surface)
        self.__draw_planets_and_player(surface, game)
        self.__draw_debug_info(surface, game)


    def __draw_debug_info(self, surface: pygame.Surface, game: StoryGame):
        """
        Draw textual debug information on the surface, including additional information.

        :param surface: The pygame.Surface to draw on.
        :param game: Reference to the StoryGame instance.
        """
        # Allgemeine Debug-Informationen (links)
        general_info = [
            "Debug Mode [D]",
            f"Fuel: {game.fuel}",
            f"Hull: {game.hull}",
            f"Pos(r={game.player_row}, c={game.player_col})",
            f"Current Planet: {game.current_planet.name if game.current_planet else 'None'}"
        ]

        # Ereignis-bezogene Debug-Informationen (rechts)
        event_info = [
            f"EventManager:",
            f"Error Count: {game.event_manager.selection_manager.error_count}"
        ]
        game_stats_info = [
            f"GameStats:",
            f"Error Count:",
            f"Inventory Items: {len(game.inventory_manager.get_items())}"
        ]

        # Debug text position
        general_info_x_pos = 10
        event_info_x_pos = 200
        game_stats_info_x_pos = 500
        y_pos = 10

        # render debug information
        self.__render_info_lines(surface, general_info, x_pos=general_info_x_pos, y_pos=y_pos)
        self.__render_info_lines(surface, event_info, x_pos=event_info_x_pos, y_pos=y_pos)
        self.__render_info_lines(surface, game_stats_info, x_pos=game_stats_info_x_pos, y_pos=y_pos)

    def __draw_sonnensystem_bg(self, surface: pygame.Surface):
        surf_w, surf_h = surface.get_size()
        img_w, img_h = self.bg_solar_system.get_size()
        ratio_surf = surf_w / surf_h
        ratio_img = img_w / img_h

        if ratio_img > ratio_surf:
            new_w = surf_w
            new_h = int(new_w / ratio_img)
        else:
            new_h = surf_h
            new_w = int(new_h * ratio_img)

        scaled = pygame.transform.smoothscale(self.bg_solar_system, (new_w, new_h))
        x_pos = (surf_w - new_w) // 2
        y_pos = (surf_h - new_h) // 2
        surface.blit(scaled, (x_pos, y_pos))

    def __draw_hex_grid(self, surface: pygame.Surface):
        for r in range(self.hex_rows):
            for c in range(self.hex_cols):
                cx, cy = self.__get_hex_center(r, c)
                points = []
                for i in range(6):
                    angle = math.radians(60 * i - 30)
                    px = cx + self.hex_radius * math.cos(angle)
                    py = cy + self.hex_radius * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(surface, Color.WHITE.value, points, 2)

    def __draw_planets_and_player(self, surface: pygame.Surface, game: "StoryGame"):
        for planet in game.data.planets:
            cx, cy = self.__get_hex_center(planet.row, planet.col)
            pygame.draw.circle(surface, (0, 255, 0), (int(cx), int(cy)), 15)
            if planet.is_fuel_planet:
                pygame.draw.circle(surface, (255, 200, 50), (int(cx), int(cy)), 10)

        px, py = self.__get_hex_center(game.player_row, game.player_col)
        pygame.draw.circle(surface, Color.PLAYER.value, (int(px), int(py)), 12)

    def __render_info_lines(self, surface: pygame.Surface, lines: List[str], x_pos: int, y_pos: int):
        """
        Helper method to render a list of debug information lines at a specified position.

        :param surface: The pygame.Surface to draw on.
        :param lines: List of strings containing debug information.
        :param x_pos: X-coordinate where the text starts.
        :param y_pos: Starting Y-coordinate for the first line.
        """
        y_offset = y_pos
        for line in lines:
            surf = self.font.render(line, True, Color.WHITE.value)
            surface.blit(surf, (x_pos, y_offset))
            y_offset += 25  # Abstand zwischen den Zeilen

    def __get_hex_center(self, row: int, col: int):
        vertical_spacing = self.hex_radius * 1.5
        horizontal_spacing = math.sqrt(3) * self.hex_radius
        center_x = self.offset_x + col * horizontal_spacing + (row % 2) * (horizontal_spacing / 2)
        center_y = self.offset_y + row * vertical_spacing
        return center_x, center_y


