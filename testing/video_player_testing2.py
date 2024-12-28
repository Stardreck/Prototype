import pyglet

# Fenster für das Intro-Video
class IntroWindow(pyglet.window.Window):
    def __init__(self, video_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video = pyglet.media.load(video_file)
        self.player = pyglet.media.Player()
        self.player.queue(self.video)
        self.player.play()
        self.set_fullscreen(True)  # Optional: Fullscreen für das Intro

    def on_draw(self):
        self.clear()
        if self.player.source and self.player.source.video_format:
            self.player.get_texture().blit(0, 0)

    def on_key_press(self, symbol, modifiers):
        # Beenden des Videos bei Tastendruck
        self.player.pause()
        pyglet.app.exit()


# Fenster für das Hauptmenü
class MenuWindow(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = pyglet.text.Label(
            "Hauptmenü\n\nDrücke [S] für Start\nDrücke [Q] für Beenden",
            font_name="Arial",
            font_size=24,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
        )

    def on_draw(self):
        self.clear()
        self.label.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.S:
            print("Spiel wird gestartet...")
            pyglet.app.exit()  # Ersetze dies später mit dem Spielstart
        elif symbol == pyglet.window.key.Q:
            print("Beende das Spiel...")
            pyglet.app.exit()


def main():
    # Intro-Fenster
    video_file = "../assets/test_video01.ogg"  # Pfad zu deinem Video
    intro_window = IntroWindow(video_file, width=800, height=600)

    # Nach dem Intro das Hauptmenü anzeigen
    def switch_to_menu(dt):
        intro_window.close()
        menu_window = MenuWindow(width=800, height=600)

    # Intro-Dauer oder Keypress überwachen
    pyglet.clock.schedule_once(switch_to_menu, intro_window.video.duration)
    pyglet.app.run()


if __name__ == "__main__":
    main()
