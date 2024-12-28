import pygame
import pygame_gui
from moviepy import VideoFileClip

class SciFiStartScreen:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen setup
        self.screen_size = (800, 600)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Sci-Fi Start Screen")

        # Load background image
        self.background_image = pygame.image.load("assets/welcome_screen.jpeg")
        self.background_image = pygame.transform.scale(self.background_image, self.screen_size)

        # Pygame GUI manager
        self.manager = pygame_gui.UIManager(self.screen_size)

        # Create GUI elements
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((250, 100), (300, 50)),
            text="Welcome to the Sci-Fi World",
            manager=self.manager,
            object_id="#title_label"
        )

        self.start_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 200), (100, 50)),
            text="Start Game",
            manager=self.manager
        )

        self.quit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((350, 300), (100, 50)),
            text="Quit",
            manager=self.manager
        )

        # Clock for managing frame rate
        self.clock = pygame.time.Clock()

        # Running state
        self.running = True

    def play_intro_video(self, video_path):
        # Load video with moviepy
        clip = VideoFileClip(video_path)

        # Extract and load audio for playback
        audio_path = "temp_audio.mp3"
        clip.audio.write_audiofile(audio_path, fps=44100)
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        pygame.mixer.music.play()

        video_fps = clip.fps  # Get the video's FPS
        frame_duration = 1 / video_fps  # Duration of each frame in seconds

        last_frame_time = pygame.time.get_ticks()

        for frame in clip.iter_frames(fps=video_fps, dtype="uint8", with_times=False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clip.close()
                    pygame.quit()
                    exit()

            # Convert frame to Pygame surface and display
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, self.screen_size)
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            # Wait to maintain video frame rate
            while (pygame.time.get_ticks() - last_frame_time) < frame_duration * 1000:
                pass
            last_frame_time = pygame.time.get_ticks()

        clip.close()
        pygame.mixer.music.stop()

    def run(self):
        # Play the intro video before showing the menu
        self.play_intro_video("assets/test_video01.mp4")

        while self.running:
            time_delta = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle GUI events
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self.start_button:
                        print("Start Game clicked!")
                    elif event.ui_element == self.quit_button:
                        print("Quit clicked!")
                        self.running = False

                self.manager.process_events(event)

            # Draw background
            self.screen.blit(self.background_image, (0, 0))

            # Update GUI
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    sci_fi_screen = SciFiStartScreen()
    sci_fi_screen.run()
