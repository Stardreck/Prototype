from pygame import Surface

from managers.view_manager import ViewManager
from plugins.video_player import VideoPlayer
from views.view import View


class IntroView(View):
    def __init__(self, screen: Surface, view_manager: ViewManager):
        super().__init__(screen, view_manager)

    def render(self):
        super()
        self.play_intro_video("assets/test_video01.mp4")


    def play_intro_video(self, video_path):
        player = VideoPlayer(self.screen)
        player.set_video(video_path)
        player.play()
