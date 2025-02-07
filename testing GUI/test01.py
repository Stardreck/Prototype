import pygame
import pygame_gui

# Konstanten
WINDOW_SIZE = (800, 600)
BACKGROUND_COLOR = (211, 211, 211)  # Leichtes Grau
PANEL_SIZE = (400, 300)
TEXTS = [
    "Dies ist die erste Nachricht.\nSie erstreckt sich über mehrere Zeilen.",
    "Dies ist die zweite Nachricht.\nAuch sie erstreckt sich über mehrere Zeilen.",
    "Dies ist die dritte Nachricht.\nSie setzt das Muster fort."
]

class MessageBox:
    """Klasse zur Verwaltung des Nachrichtenfelds mit Text und einem Button."""
    def __init__(self, manager, text):
        self.manager = manager
        self.text = text
        self.create_ui_elements()

    def create_ui_elements(self):
        """Erstellt das Panel, das Textfeld und den Button und zentriert sie auf dem Bildschirm."""
        # Panel erstellen
        self.panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), PANEL_SIZE),
            manager=self.manager,
            object_id="#message_panel"
        )
        self.panel.set_relative_position((
            (WINDOW_SIZE[0] - PANEL_SIZE[0]) // 2,
            (WINDOW_SIZE[1] - PANEL_SIZE[1]) // 2
        ))

        # Textfeld im Panel erstellen
        self.text_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect((10, 10), (PANEL_SIZE[0] - 20, PANEL_SIZE[1] - 70)),
            html_text=self.text,
            manager=self.manager,
            container=self.panel,
            object_id="#text_box"
        )

        # 'Weiter'-Button im Panel erstellen
        self.next_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((0, 0), (100, 50)),
            text="Weiter",
            manager=self.manager,
            container=self.panel,
            object_id="#weiter_button"
        )
        self.next_button.set_relative_position((
            (PANEL_SIZE[0] - 100) // 2,
            PANEL_SIZE[1] - 60
        ))

    def destroy(self):
        """Entfernt die UI-Elemente vom Manager."""
        self.panel.kill()

def main():
    """Hauptfunktion zum Ausführen der Anwendung."""
    pygame.init()
    window_surface = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption('Nachrichtenfeld Prototyp')

    manager = pygame_gui.UIManager(WINDOW_SIZE, 'theme.json')

    clock = pygame.time.Clock()
    is_running = True
    message_index = 0

    # Erstes Nachrichtenfeld erstellen
    message_box = MessageBox(manager, TEXTS[message_index])

    while is_running:
        time_delta = clock.tick(60) / 1000.0  # Begrenzung auf 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                print("UI_BUTTON_PRESSED")
                if event.ui_element == message_box.next_button:
                    print("Button clicked")
                    message_box.destroy()
                    message_index = (message_index + 1) % len(TEXTS)
                    message_box = MessageBox(manager, TEXTS[message_index])

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.fill(BACKGROUND_COLOR)
        manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
