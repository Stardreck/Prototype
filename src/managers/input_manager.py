import pygame

class InputManager:
    """
    Handles user input and delegates actions to the game logic.
    """
    def __init__(self, game):
        """
        Initializes the InputManager with a reference to the game instance.
        :param game: The game instance that will receive input events.
        """
        self.game = game

    def process_events(self):
        """
        Processes all incoming events and triggers corresponding game actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.stop()
            elif event.type == pygame.KEYDOWN:
                self.handle_keydown(event)

    def handle_keydown(self, event):
        """
        Handles keydown events and triggers game-specific actions.
        :param event: The pygame.KEYDOWN event.
        """
        if event.key == pygame.K_ESCAPE:
            self.game.stop()
        elif event.key == pygame.K_d:
            self.game.debug_manager.toggle_debug_mode()

        else:
            self.game.handle_movement(event)
        #
        # elif event.key == pygame.K_UP:
        #     self.game.move_player(-1, 0)
        # elif event.key == pygame.K_DOWN:
        #     self.game.move_player(1, 0)
        # elif event.key == pygame.K_LEFT:
        #     self.game.move_player(0, -1)
        # elif event.key == pygame.K_RIGHT:
        #     self.game.move_player(0, 1)