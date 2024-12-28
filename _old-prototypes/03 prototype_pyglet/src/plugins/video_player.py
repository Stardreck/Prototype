from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

class VideoPlayer(Screen):
    def __init__(self, video_source, next_screen, **kwargs):
        super().__init__(**kwargs)
        self.video_source = video_source
        self.next_screen = next_screen

        # Video ohne Steuerelemente
        self.video = Video(source=self.video_source)
        self.video.state = "play"  # Startet das Video automatisch
        self.add_widget(self.video)

        # Überwacht die Zeit und prüft, ob das Video fertig ist
        Clock.schedule_interval(self.check_video_status, 0.5)

        # Füge Key-Event Listener hinzu
        Window.bind(on_key_down=self.skip_video)

    def check_video_status(self, dt):
        # Prüfen, ob das Video fertig ist
        if self.video.state == "stop":
            self.goto_next_screen()

    def skip_video(self, *args):
        # Direkt zum nächsten Bildschirm wechseln, wenn eine Taste gedrückt wird
        self.goto_next_screen()

    def goto_next_screen(self):
        self.video.state = "stop"  # Stoppt das Video
        self.remove_widget(self.video)  # Entfernt das Video-Widget
        self.manager.current = self.next_screen  # Wechsel zum nächsten Bildschirm
        Clock.unschedule(self.check_video_status)  # Stoppt die Überwachung
        Window.unbind(on_key_down=self.skip_video)  # Entfernt den Key-Event Listener