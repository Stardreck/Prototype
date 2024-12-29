import pygame
import pygame_gui
import os

class SciFiMainMenu:
    def __init__(self):
        pygame.init()

        # Überprüfe, ob die JSON-Datei existiert
        theme_path = "theme/gui.json"
        if not os.path.exists(theme_path):
            print(f"Theme-Datei nicht gefunden: {theme_path}")
        else:
            print(f"Theme-Datei gefunden: {theme_path}")

        # Screen setup
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Sci-Fi Hauptmenü")

        # Pygame GUI manager
        self.manager = pygame_gui.UIManager(self.screen_size, theme_path=theme_path)

        # Background image
        self.background_image = pygame.image.load("assets/welcome_screen.jpeg")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)

        # Create GUI elements
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((200, 50), (400, 70)),
            text="Stardreck",
            manager=self.manager,
            object_id="#main_menu_title"
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 200), (200, 50)),
            text="Reise beginnen",
            manager=self.manager,
        )

        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((300, 300), (200, 50)),
            text="Einstellungen",
            manager=self.manager
        )

        # Clock
        self.clock = pygame.time.Clock()

        # State
        self.running = True

    def run(self):
        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle button clicks
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print("Reise beginnt!")
                    elif event.ui_element == self.settings_button:
                        print("Einstellungen öffnen")

                self.manager.process_events(event)

            # Draw background
            self.screen.blit(self.background_image, (0, 0))

            # Update GUI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    sci_fi_menu = SciFiMainMenu()
    sci_fi_menu.run()
