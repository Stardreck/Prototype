import pygame

from src.star_config import StarConfig
from views.intro_view import IntroView


class StarEngine:
    def __init__(self):
        self.config: StarConfig | None = None

        # Initialize Pygame
        pygame.init()

        # Screen setup
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Star Engine - Pygame")

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # State variables
        self.is_running = True

    """
    Updates the game state. This method is called 60 times per second by default.

    Args:
        delta_time (float): The time in seconds since the last update call.
    """
    def update(self, delta_time: float):
        # TODO: Update game state here
        # Example: Print delta_time for debugging
        # print(f"Delta Time: {delta_time}")
        pass

    """
    Renders the game content onto the screen. Called whenever the screen needs to be redrawn.
    """
    def on_draw(self):
        # Clear the screen with a color (e.g., black)
        self.screen.fill((0, 0, 0))

        # TODO: Add drawing code here
        # Example: Draw a simple rectangle
        pygame.draw.rect(self.screen, (0, 255, 0), (100, 100, 200, 150))

        # Update the display
        pygame.display.flip()

    """
    Handles key press events. Called when a key is pressed.

    Args:
        event (pygame.event.Event): The key press event.
    """
    def on_key_press(self, event):
        print(f"Key pressed: {event.key}")

        # Example: Quit the game on pressing ESC
        if event.key == pygame.K_ESCAPE:
            self.is_running = False

    def play_intro(self):
        intro = IntroView(self.screen)
        intro.render()

    """
    Main game loop. Starts the game and runs the update and draw methods in a loop.
    """
    def run(self):
        # play the game intro video
        self.play_intro()

        # main game loop
        while self.is_running:
            # Calculate delta_time
            delta_time = self.clock.tick(60) / 1000.0  # 60 FPS, convert milliseconds to seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    self.on_key_press(event)

            # Update the game state
            self.update(delta_time)

            # Render the screen
            self.on_draw()

        # Quit application
        pygame.quit()