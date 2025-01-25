import os
import sys

import pygame
from moviepy import VideoFileClip
from pygame import Surface


class VideoPlayer:
    """
    Plays a video file (MP4) including audio
    skips the video on a key pressed event
    """
    def __init__(self, screen: Surface | None):
        self.screen = screen
        self.video_path = None
        self.temp_folder = "temp"
        self.temp_audio_path = os.path.join(self.temp_folder, "temp_audio.mp3")

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder, exist_ok=True)

    def enable_standalone(self, width: int, height: int, title: str):
        """
        Use the VideoPlayer as a standalone window, without prior initialization of pygame
        """
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)


    def set_video(self, video_path: str):
        self.video_path = video_path

    def __render(self, clip: VideoFileClip):
        frame_duration = 1 / clip.fps
        last_frame_time = pygame.time.get_ticks()

        pygame.mixer.music.play()

        for frame in clip.iter_frames(fps=clip.fps, dtype="uint8", with_times=False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clip.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    clip.close()
                    pygame.mixer.music.stop()
                    return

            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, self.screen.get_size())
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            while (pygame.time.get_ticks() - last_frame_time) < frame_duration * 1000:
                pass
            last_frame_time = pygame.time.get_ticks()

    def play(self):
        if not self.video_path:
            print("Kein Video angegeben!")
            return

        clip = VideoFileClip(self.video_path)

        # Audio extrahieren
        clip.audio.write_audiofile(self.temp_audio_path, fps=44100)
        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_audio_path)

        self.__render(clip)

        clip.close()
        pygame.mixer.music.stop()