import pygame, sys
import pygame_gui
from pygame import Surface

from managers.view_manager import ViewManager
from views.view import View


class MainView(View):
    def __init__(self, screen: Surface, view_manager: ViewManager):
        super().__init__(screen, view_manager)
        self.start_button = None
        self.settings_button = None

    def render(self):
        super()

        screen_width, screen_height = self.screen.get_size()
        button_width, button_height = 200, 50
        button_spacing = 20  # Abstand zwischen Buttons
        label_height = 100


        # Create GUI elements
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 500 // 2, screen_height // 2 - 200),  # X, Y
                (500, label_height),  # width, height
            ),
            text="Stardreck",
            manager=self.UIManager,
            object_id="#main_menu_title"
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - button_width // 2, screen_height // 2 - button_height // 2),
                (button_width, button_height),
            ),
            text="Reise beginnen",
            manager=self.UIManager,
        )

        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - button_width // 2, screen_height // 2 + button_height + button_spacing),
                (button_width, button_height),
            ),
            text="Einstellungen",
            manager=self.UIManager
        )

        self.set_background_image("assets/welcome_screen.png")

        while self.is_visible:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_visible = False
                # Handle button clicks
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print("Reise beginnt!")
                        self.is_visible = False
                    elif event.ui_element == self.settings_button:
                        print("Einstellungen öffnen")
                        self.view_manager.set_view("settings")
                        self.is_visible = False

                self.UIManager.process_events(event)

            # Draw background
            self.screen.blit(self.background_surface, (0, 0))

            # Update GUI
            self.UIManager.update(time_delta)
            self.UIManager.draw_ui(self.screen)

            pygame.display.flip()

        return True