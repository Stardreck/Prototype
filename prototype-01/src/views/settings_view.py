import pygame
import pygame_gui
from pygame import Surface
from views.view import View
from managers.view_manager import ViewManager


class SettingsView(View):
    def __init__(self, screen: Surface, view_manager: ViewManager):
        super().__init__(screen, view_manager)
        self.brightness_slider = None
        self.back_button = None

    def render(self):
        super()

        screen_width, screen_height = self.screen.get_size()
        slider_width, slider_height = 300, 50
        button_width, button_height = 200, 50
        label_height = 100
        spacing = 20

        # Titel hinzufügen
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(
                (screen_width // 2 - 500 // 2, screen_height // 2 - 200),  # X, Y
                (500, label_height),  # width, height
            ),
            text="Einstellungen",
            manager=self.UIManager,
            object_id="#settings_menu_title"
        )

        # Slider für Helligkeit
        self.brightness_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(
                (screen_width // 2 - slider_width // 2, screen_height // 2 - slider_height // 2),
                (slider_width, slider_height),
            ),
            start_value=50,  # Standardwert
            value_range=(0, 100),
            manager=self.UIManager,
        )

        # Zurück-Button
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (screen_width // 2 - button_width // 2, screen_height // 2 + slider_height + spacing),
                (button_width, button_height),
            ),
            text="Zurück",
            manager=self.UIManager,
        )

        self.set_background_image("assets/welcome_screen.png")

        while self.is_visible:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_visible = False
                    return False

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.back_button:
                        print("Zurück zum Hauptmenü")
                        self.view_manager.set_view("main")
                        self.is_visible = False

                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.brightness_slider:
                        print(f"Helligkeit: {event.value}")

                self.UIManager.process_events(event)

            # Hintergrund zeichnen
            self.screen.blit(self.background_surface, (0, 0))

            # GUI aktualisieren
            self.UIManager.update(time_delta)
            self.UIManager.draw_ui(self.screen)

            pygame.display.flip()

        return True
