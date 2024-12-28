import pygame
from moviepy import VideoFileClip
from pygame import Surface


class VideoPlayer:
    def __init__(self, screen: Surface):
        self.screen: Surface = screen
        self.video_path: str | None = None
        self.temp_folder: str = "temp"
        self.temp_audio_path: str = self.temp_folder + "/temp_audio.mp3"

    def set_video(self, video_path):
        self.video_path = video_path

    def __render(self, video):

        frame_duration = 1 / video.fps  # Duration of each frame in seconds
        last_frame_time = pygame.time.get_ticks()

        #play audio
        pygame.mixer.music.play()
        # render video frames
        for frame in video.iter_frames(fps=video.fps, dtype="uint8", with_times=False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # stop video if window is closed
                    video.close()
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    # Skip the video when any key is pressed
                    video.close()
                    pygame.mixer.music.stop()
                    return

            # Convert frame to Pygame surface and display
            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, self.screen.get_size())
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            # Wait to maintain video frame rate
            while (pygame.time.get_ticks() - last_frame_time) < frame_duration * 1000:
                pass
            last_frame_time = pygame.time.get_ticks()

    def play(self):
        # init video file
        video = VideoFileClip(self.video_path)

        # Extract and load audio for playback
        video.audio.write_audiofile(self.temp_audio_path, fps=44100)
        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_audio_path)

        # play video with audio
        self.__render(video)

        # video played, destruct objects
        video.close()
        pygame.mixer.music.stop()
