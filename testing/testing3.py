import pyglet
from pyglet.window import key

class MainMenu:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()

        # Hintergrundvideo mit Ton
        self.player = pyglet.media.Player()
        self.source = pyglet.media.load('assets/test_video01.mp4')
        self.player.queue(self.source)
        self.player.loop = True
        self.player.play()

        # Animierter Text
        self.text_label = pyglet.text.Label(
            "Stardreck",
            font_name='Arial',
            font_size=48,
            x=self.window.width // 2,
            y=self.window.height - 150,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        self.text_animation = 0

        # Schaltfläche "Reise beginnen"
        self.button_label = pyglet.text.Label(
            "Reise beginnen",
            font_name='Arial',
            font_size=24,
            x=self.window.width // 2,
            y=100,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )
        self.button_hover = False

    def update(self, dt):
        # Animiert den Text
        self.text_animation += dt
        scale = 1.0 + 0.1 * pyglet.math.sin(self.text_animation * 2)
        self.text_label.font_size = int(48 * scale)

    def render(self):
        self.window.clear()
        self.player.get_texture().blit(0, 0)
        self.batch.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        # Überprüft, ob die Maus über der Schaltfläche ist
        button_x_start = self.button_label.x - self.button_label.content_width // 2
        button_x_end = self.button_label.x + self.button_label.content_width // 2
        button_y_start = self.button_label.y - self.button_label.content_height // 2
        button_y_end = self.button_label.y + self.button_label.content_height // 2

        self.button_hover = button_x_start <= x <= button_x_end and button_y_start <= y <= button_y_end
        if self.button_hover:
            self.button_label.color = (200, 50, 50, 255)  # Rot bei Hover
        else:
            self.button_label.color = (255, 255, 255, 255)  # Weiß normal

    def on_mouse_press(self, x, y, button, modifiers):
        if self.button_hover:
            # Wechsel zu den Spieleinstellungen
            self.player.pause()  # Stoppt das Video
            return "settings"
        return None

class SettingsView:
    def __init__(self, window):
        self.window = window
        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            "Spieleinstellungen",
            font_name='Arial',
            font_size=36,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch
        )

    def render(self):
        self.window.clear()
        self.batch.draw()

class StardreckApp:
    def __init__(self):
        self.window = pyglet.window.Window(800, 600, "Stardreck")
        self.current_view = MainMenu(self.window)
        self.settings_view = SettingsView(self.window)

    def run(self):
        pyglet.clock.schedule_interval(self.update, 1/60.0)

        @self.window.event
        def on_draw():
            self.current_view.render()

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            if isinstance(self.current_view, MainMenu):
                self.current_view.on_mouse_motion(x, y, dx, dy)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            if isinstance(self.current_view, MainMenu):
                next_view = self.current_view.on_mouse_press(x, y, button, modifiers)
                if next_view == "settings":
                    self.current_view = self.settings_view

    def update(self, dt):
        if isinstance(self.current_view, MainMenu):
            self.current_view.update(dt)

if __name__ == "__main__":
    app = StardreckApp()
    app.run()
