import pyglet

# Shared Components
class AudioManager:
    def __init__(self):
        self.sounds = {}

    def load_sound(self, name, path):
        self.sounds[name] = pyglet.media.load(path, streaming=False)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].play()

class DisplayManager:
    def __init__(self, width=800, height=600, title="Interactive Board Game"):
        self.window = pyglet.window.Window(width, height, title)
        self.background = None

    def set_background(self, path):
        self.background = pyglet.resource.image(path)

    def render_text(self, text, x, y, font_size=20):
        label = pyglet.text.Label(
            text,
            font_name='Arial',
            font_size=font_size,
            x=x, y=y,
            anchor_x='center', anchor_y='center'
        )
        label.draw()

    def render(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            if self.background:
                self.background.blit(0, 0)
            self.render_text("Select a Game Mode", self.window.width // 2, self.window.height - 50, font_size=24)

class GameMode:
    def __init__(self, name):
        self.name = name

    def start(self):
        raise NotImplementedError("Each game mode must implement the start method.")

# Game Modes
class ClassicMode(GameMode):
    def __init__(self):
        super().__init__("Classic Mode")

    def start(self):
        print("Starting Classic Mode")

class AlternativeMode(GameMode):
    def __init__(self):
        super().__init__("Alternative Mode")

    def start(self):
        print("Starting Alternative Mode")

class ArcadeMode(GameMode):
    def __init__(self):
        super().__init__("Arcade Mode")

    def start(self):
        print("Starting Arcade Mode")

# Launcher
class GameLauncher:
    def __init__(self):
        self.modes = [
            ClassicMode(),
            AlternativeMode(),
            ArcadeMode()
        ]
        self.display_manager = DisplayManager()
        self.display_manager.set_background("assets/welcome_screen.jpeg")
        self.audio_manager = AudioManager()

    def list_modes(self):
        print("Available Modes:")
        for i, mode in enumerate(self.modes):
            print(f"{i + 1}. {mode.name}")

    def select_mode(self, index):
        if 0 <= index < len(self.modes):
            self.modes[index].start()
        else:
            print("Invalid selection.")

    def run(self):
        @self.display_manager.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key._1:
                self.modes[0].start()
            elif symbol == pyglet.window.key._2:
                self.modes[1].start()
            elif symbol == pyglet.window.key._3:
                self.modes[2].start()
            else:
                print("Invalid Key. Press 1, 2, or 3.")

        self.display_manager.render()
        pyglet.app.run()

# Main Execution
if __name__ == "__main__":
    launcher = GameLauncher()
    launcher.run()
