import pygame

from board_game_test import DebugManager
from data.settings import TILE_SIZE, RED, BOARD_COLS, BOARD_ROWS, MARGIN_TOP


class Player(pygame.sprite.Sprite):
    def __init__(self, game_width: int, game_height: int):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()


        self.board_x = 0
        self.board_y = 0
        self.ship_x  = 0
        self.ship_y  = 0
        self.game_width  = game_width
        self.game_height = game_height
        self.update_system_position()

    def move_system_map(self, pos_x: int, pos_y: int):
        x = self.board_x + pos_x
        y = self.board_y + pos_y
        if 0 <= x < BOARD_COLS and 0 <= y < BOARD_ROWS:
            self.board_x = x
            self.board_y = y
            self.update_system_position()
            return True
        return False

    def move_ship_map(self):
        pass

    def update_system_position(self):
        offset_x = (self.game_width // 2 - BOARD_COLS * TILE_SIZE) // 2
        offset_y = MARGIN_TOP
        self.rect.x = offset_x + self.board_x * TILE_SIZE
        self.rect.y = offset_y + self.board_y * TILE_SIZE

    def update_ship_position(self):
        pass
