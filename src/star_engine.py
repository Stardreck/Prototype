import pathlib
import sys
import pygame

from enums.color import Color
from games.game import Game




class StarEngine:
    def __init__(self):

        ##### init pygame #####
        pygame.init()
        self.width = 1600
        self.height = 720
        self.fps = 60
        self.title = "StarDreck"
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.is_running = True

        # fully qualified src directory path
        self.src_dir = pathlib.Path(__file__).resolve().parent.parent

        ##### Fonts #####
        # get starjedi fully qualified path
        self.font_starjedi_path = self.src_dir.joinpath("assets", "fonts", "StarJedi", "Starjedi.ttf")
        self.title_font = pygame.font.Font(str(self.font_starjedi_path), 64)
        self.menu_font = pygame.font.SysFont(None, 36)

    def show_main_menu(self):
            """
            Main Menu
            returns the game to play or "quit"
            """
            button_width = 250
            button_height = 60
            button_x = (self.width - button_width) // 2
            button_y = (self.height - button_height) // 2

            while True:
                dt = self.clock.tick(self.fps) / 1000.0
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.is_running = False
                        return "quit"
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:  # Linksklick
                            mx, my = event.pos
                            if (button_x <= mx <= button_x + button_width and
                                    button_y <= my <= button_y + button_height):
                                return "storygame"

                # Hintergrund
                self.screen.fill(Color.GAME_BG.value)

                # Titel
                title_surf = self.title_font.render("Stardreck", True, Color.WHITE.value)
                title_rect = title_surf.get_rect(center=(self.width // 2, 100))
                self.screen.blit(title_surf, title_rect)

                # Button
                mx, my = pygame.mouse.get_pos()
                if (button_x <= mx <= button_x + button_width and
                        button_y <= my <= button_y + button_height):
                    pygame.draw.rect(self.screen, Color.BUTTON_HOVER.value,
                                     (button_x, button_y, button_width, button_height))
                else:
                    pygame.draw.rect(self.screen, Color.BUTTON_BG.value,
                                     (button_x, button_y, button_width, button_height))

                text_surf = self.menu_font.render("Reise beginnen", True, Color.WHITE.value)
                text_rect = text_surf.get_rect(center=(button_x + button_width // 2,
                                                       button_y + button_height // 2))
                self.screen.blit(text_surf, text_rect)

                pygame.display.flip()


    def run(self, game: Game):
        """
        Main Loop
        calls the active game methods
        """
        while self.is_running and game.is_running:
            delta_time = self.clock.tick(self.fps) / 1000.0
            game.handle_events()
            game.update(delta_time)
            game.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()
