from kivy.app import App
from kivy.uix.video import Video
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window

class VideoPlayerScreen(Screen):
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

class MenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        # Begrüßungstext
        label = Label(text="Willkommen im Hauptmenü", font_size=32)
        layout.add_widget(label)

        # Button: Spiel starten
        start_button = Button(text="Spiel starten", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5})
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)

        # Button: Beenden
        quit_button = Button(text="Beenden", size_hint=(0.5, 0.2), pos_hint={"center_x": 0.5})
        quit_button.bind(on_press=self.quit_game)
        layout.add_widget(quit_button)

        self.add_widget(layout)

    def start_game(self, instance):
        print("Spiel wird gestartet...")  # Hier kannst du die Spiel-Logik starten
        # Falls du einen Spiel-Screen hinzufügen möchtest, stelle sicher, dass er existiert
        if "game" in self.manager.screen_names:
            self.manager.current = "game"
        else:
            print("Fehler: Kein Screen mit dem Namen 'game' vorhanden.")

    def quit_game(self, instance):
        App.get_running_app().stop()  # Beendet die Anwendung

class MyApp(App):
    def build(self):
        # ScreenManager für die Navigation zwischen den Bildschirmen
        sm = ScreenManager()

        sm.add_widget(VideoPlayerScreen(video_source="../assets/test_video01.mp4", next_screen="menu", name="intro"))
        sm.add_widget(MenuScreen(name="menu"))

        # Starte mit dem Intro
        return sm

if __name__ == "__main__":
    MyApp().run()
