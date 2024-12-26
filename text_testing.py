import pyglet

class SimpleUI:
    def __init__(self):
        self.window = pyglet.window.Window(800, 600, "Text and Button Example")

        # UI Elements
        self.batch = pyglet.graphics.Batch()

        # Black semi-transparent rectangle behind the text
        self.text_background = pyglet.shapes.Rectangle(
            x=0,
            y=self.window.height // 2 - 50,
            width=self.window.width,
            height=100,
            color=(0, 0, 0),
            batch=self.batch
        )
        self.text_background.opacity = 100  # 0.4 opacity

        # Centered text
        self.text_label = pyglet.text.Label(
            "Willkommen bei Stardreck!",
            font_name='Arial',
            font_size=36,
            x=self.window.width // 2,
            y=self.window.height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            batch=self.batch
        )

        # Button background with rounded corners
        self.button_background = pyglet.shapes.Rectangle(
            x=self.window.width // 2 - 120,
            y=self.window.height // 2 - 140,
            width=240,
            height=50,
            color=(50, 150, 255),
            batch=self.batch
        )
        self.button_background.opacity = 255  # Fully opaque

        # Button label
        self.button_label = pyglet.text.Label(
            "Reise beginnen",
            font_name='Arial',
            font_size=24,
            x=self.window.width // 2,
            y=self.window.height // 2 - 115,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255),
            batch=self.batch
        )
        self.button_hover = False

        # Event Handling
        @self.window.event
        def on_draw():
            self.window.clear()
            self.text_background.draw()
            self.button_background.draw()
            self.batch.draw()

        @self.window.event
        def on_mouse_motion(x, y, dx, dy):
            self.handle_mouse_hover(x, y)

        @self.window.event
        def on_mouse_press(x, y, button, modifiers):
            self.handle_mouse_click(x, y)

        pyglet.clock.schedule_interval(self.update, 1/60.0)

    def handle_mouse_hover(self, x, y):
        button_x_start = self.button_background.x
        button_x_end = self.button_background.x + self.button_background.width
        button_y_start = self.button_background.y
        button_y_end = self.button_background.y + self.button_background.height

        self.button_hover = button_x_start <= x <= button_x_end and button_y_start <= y <= button_y_end
        self.button_background.color = (30, 120, 220) if self.button_hover else (50, 150, 255)

    def handle_mouse_click(self, x, y):
        if self.button_hover:
            print("Reise beginnt!")
            self.open_settings_view()

    def open_settings_view(self):
        print("Wechsel zu Spieleinstellungen...")
        self.text_background.opacity = 0  # Hide background
        self.text_label.text = "Spieleinstellungen"
        self.text_label.y = self.window.height // 2  # Center new text
        self.button_background.opacity = 0
        self.button_label.text = ""

    def update(self, dt):
        pass  # Updates handled by Pyglet

    def run(self):
        pyglet.app.run()

if __name__ == "__main__":
    app = SimpleUI()
    app.run()