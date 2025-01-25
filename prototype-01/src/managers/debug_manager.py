# debug_manager.py
from typing import TYPE_CHECKING
import pygame
from pygame import Surface

from data.settings import WHITE, BLACK, GRAY, GREEN, PURPLE, BOARD_COLS, BOARD_ROWS, TILE_SIZE, MARGIN_TOP, SHIP_INTERIOR_COLS, SHIP_INTERIOR_ROWS
from star_engine import StarEngine

if TYPE_CHECKING:
    from games.story_game import StoryGame  # for type hints


class DebugManager:
    def __init__(self, screen: Surface):
        self.debug_mode = False
        self.screen = screen

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        print(f"Debug mode: {self.debug_mode}")

    def is_debug_active(self):
        return self.debug_mode


    def create_surfaces(self, game):
        if self.debug_mode:
            board_rect = pygame.Rect(0, 0, game.width // 2, game.height)
            overlay_rect = pygame.Rect(game.width // 2, 0, game.width // 2, game.height)
            game.board_surface = game.screen.subsurface(board_rect)
            game.overlay_surface = game.screen.subsurface(overlay_rect)
        else:
            full_rect = pygame.Rect(0, 0, game.width, game.height)
            game.board_surface = None
            game.overlay_surface = game.screen.subsurface(full_rect)

    def draw_system_map_debug(self, game: "StoryGame") -> None:
        if not game.board_surface:
            return
        board_surface = game.board_surface
        board_surface.fill(WHITE)

        ox = (board_surface.get_width() - BOARD_COLS*TILE_SIZE)//2
        oy = MARGIN_TOP
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                rect=pygame.Rect(ox + c*TILE_SIZE, oy + r*TILE_SIZE, TILE_SIZE,TILE_SIZE)
                pygame.draw.rect(board_surface, GRAY, rect,1)

        for planet in game.planets:
            px, py = planet["pos"]
            cx = ox + px*TILE_SIZE + TILE_SIZE//2
            cy = oy + py*TILE_SIZE + TILE_SIZE//2
            color = PURPLE if planet.get("is_fuel_planet",False) else (GREEN if not planet["visited"] else (100,200,100))
            pygame.draw.circle(board_surface, color,(cx,cy),15)

        game.all_sprites.draw(board_surface)

        line_y=20
        txt_fuel = pygame.font.Font().render(f"Fuel: {game.fuel}", True, BLACK)
        board_surface.blit(txt_fuel,(20,line_y))
        line_y+=30
        txt_hull = pygame.font.Font().render(f"Hull: {game.hull}", True, BLACK)
        board_surface.blit(txt_hull,(20,line_y))
        line_y+=30