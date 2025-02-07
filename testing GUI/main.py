from typing import Callable

import pygame
import pygame_gui
from pygame_gui.core import IContainerLikeInterface, UIElement
from pygame_gui.core.gui_type_hints import RectLike
from pygame_gui.elements import UIWindow

PANEL_SIZE = (525, 399)


class UIPanel(pygame_gui.elements.UIPanel):
    def __init__(self, relative_rect: RectLike, manager: pygame_gui.UIManager, object_id: str | None = None,
                 container: IContainerLikeInterface | None = None):
        super().__init__(relative_rect, manager=manager, container=container,
                         object_id=object_id)


class UITextBox(pygame_gui.elements.UITextBox):
    def __init__(self, html_text: str, relative_rect: RectLike, manager: pygame_gui.UIManager,
                 container: IContainerLikeInterface, object_id: str | None = None, anchors: dict[str, str | UIElement] | None = None):
        super().__init__(html_text=html_text, relative_rect=relative_rect, manager=manager, container=container,
                         object_id=object_id, anchors=anchors)


class UIButton(pygame_gui.elements.UIButton):
    def __init__(self, text: str, relative_rect: RectLike, manager: pygame_gui.UIManager,
                 container: IContainerLikeInterface, object_id: str | None = None, anchors: dict[str, str | UIElement] | None = None):
        super().__init__(text=text, relative_rect=relative_rect, manager=manager, container=container,
                         object_id=object_id, anchors=anchors, )

    def set_event(self, event: int, function: Callable = None):
        """
        Bind a function to an element event.

        :param event: The event to bind. For example, pygame_gui.UI_BUTTON_PRESSED

        :param function: The function to bind. None to unbind.

        """
        self.bind(event, function)


class Game:
    def __init__(self):
        self.is_running = True
        self.manager = pygame_gui.UIManager((1600, 720), 'theme.json')
        self.manager.set_visual_debug_mode(True)
        self.index = 0

    def test(self, data):
        print("function called!!", self.index, "Data: ", data)
        self.index = self.index + 1

    def show_menu(self):
        # https://pygame-gui.readthedocs.io/en/v_067/layout_guide.html

        panel = UIPanel(relative_rect=pygame.Rect(250, 100, 545, 473),
                        manager=self.manager,
                        )

        text = UITextBox(relative_rect=pygame.Rect((0, 50), (400,200)),
                         html_text="Dies ist die erste Nachricht.\nSie erstreckt sich über mehrere Zeilen.",
                         anchors={"center": "center"},
                         manager=self.manager,
                         container=panel,
                         )

        button = UIButton(relative_rect=pygame.Rect((0, -50), (250, 40)),
                          text="Weiter",
                          manager=self.manager,
                          container=panel,
                          anchors={'centerx': 'centerx', 'bottom': 'bottom'},
                          )



        testData = 150
        button.set_event(pygame_gui.UI_BUTTON_PRESSED, lambda: self.test(testData))


def main():
    pygame.init()
    pygame.display.set_caption('Nachrichtenfeld Prototyp')

    window_surface = pygame.display.set_mode((1600, 720))

    clock = pygame.time.Clock()

    game = Game()
    game.show_menu()

    while game.is_running:
        time_delta = clock.tick(60) / 1000.0  # limit to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.is_running = False
            game.manager.process_events(event)



        game.manager.update(time_delta)

        window_surface.fill((211, 211, 211))
        game.manager.draw_ui(window_surface)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
