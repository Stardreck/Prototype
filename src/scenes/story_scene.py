import pygame
from pygame import Surface

from managers.view_manager import ViewManager
from scenes.scene import Scene


class StoryScene(Scene):
    def __init__(self, screen: Surface, view_manager: ViewManager):
        super().__init__(screen, view_manager)

    def render(self):
        timer = pygame.time.Clock()
        messages = ["Hello there! ",
                    "Ich weiss au nöd was ich da ane schriebe söll",
                    "ich schrieb eifach irgend en gaggi da ane",
                    "MUHAHAHAHA"]
        font = pygame.font.Font("freesansbold.ttf", 24)
        snip = font.render('', True, 'white')
        counter = 0
        speed = 60
        active_message = 0
        message = messages[active_message]
        done = False

        # Position and dimensions adjusted for 1600x720
        text_box_x = 0
        text_box_height = 100
        text_box_y = self.screen.get_height() - text_box_height
        text_box_width = self.screen.get_width()
        text_position_x = text_box_x + 20
        text_position_y = text_box_y + (text_box_height // 2) - font.get_height() // 2  # Center text vertically



        self.set_background_image("assets/welcome_screen.png")
        while self.is_visible:
            self.screen.blit(self.background_surface, (0, 0))
            pygame.draw.rect(self.screen, 'black', [text_box_x, text_box_y, text_box_width, text_box_height])
            if counter < speed * len(message):
                counter += 1
            elif counter >= speed * len(message):
                done = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    isRunning = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and done and active_message < len(messages):
                        active_message += 1
                        done = False
                        message = messages[active_message]
                        counter = 0
            snip = font.render(message[0:counter // speed], True, 'white')
            self.screen.blit(snip, (text_position_x, text_position_y))

            pygame.display.flip()

        pygame.quit()
