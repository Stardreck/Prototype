import vlc
import pyglet

class VideoPlayer:
    def __init__(self, window, video_path, on_complete_callback=None):
        """
        VideoPlayer ist eine Klasse, um Videos mit VLC abzuspielen.

        :param window: Das Pyglet-Fenster, in dem das Video angezeigt wird
        :param video_path: Pfad zum Video
        :param on_complete_callback: Funktion, die nach dem Video aufgerufen wird
        """
        self.window = window
        self.video_path = video_path
        self.on_complete_callback = on_complete_callback
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)
        self.player.set_hwnd(self.window._hwnd if hasattr(self.window, '_hwnd') else self.window.canvas.holder)

        # Startet das Video
        self.player.play()
        pyglet.clock.schedule_interval(self.check_video_state, 1 / 60.0)

    def check_video_state(self, dt):
        """Prüft, ob das Video beendet wurde."""
        if self.player.get_state() in [vlc.State.Ended, vlc.State.Stopped]:
            pyglet.clock.unschedule(self.check_video_state)
            self.player.stop()
            if self.on_complete_callback:
                self.on_complete_callback()

class MainMenu:
    def __init__(self, window):
        """Hauptmenü-Klasse"""
        self.window = window
        self.batch = pyglet.graphics.Batch()

        # Text
        self.text_label = pyglet.text.Label(
            "Willkommen im Hauptmenü!",
            font_name="Arial",
            font_size=36,
            x=self.window.width // 2,
            y=self.window.height - 100,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
            batch=self.batch
        )

        # Schaltfläche
        self.button_background = pyglet.shapes.Rectangle(
            x=self.window.width // 2 - 120,
            y=75,
            width=240,
            height=50,
            color=(50, 150, 255),
            batch=self.batch
        )

        self.button_label = pyglet.text.Label(
            "Spiel starten",
            font_name="Arial",
            font_size=24,
            x=self.window.width // 2,
            y=100,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
            batch=self.batch
        )

        self.button_hover = False

        self.window.push_handlers(self)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        button_x_start = self.button_background.x
        button_x_end = self.button_background.x + self.button_background.width
        button_y_start = self.button_background.y
        button_y_end = self.button_background.y + self.button_background.height

        self.button_hover = button_x_start <= x <= button_x_end and button_y_start <= y <= button_y_end
        self.button_background.color = (30, 120, 220) if self.button_hover else (50, 150, 255)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.button_hover:
            print("Spiel gestartet!")

# Callback, um nach dem Video das Hauptmenü zu starten
def start_main_menu(window):
    window.clear()
    window.remove_handlers()
    main_menu = MainMenu(window)
    window.push_handlers(main_menu)

# Hauptprogramm starten
if __name__ == "__main__":
    window = pyglet.window.Window(800, 600, "Spiel")
    video_player = VideoPlayer(window, "../assets/test_video01.mp4", on_complete_callback=lambda: start_main_menu(window))
    pyglet.app.run()
