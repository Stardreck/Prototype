from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.properties import NumericProperty
import random

# Spielkonfiguration
GRID_SIZE = 20
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400

Window.size = (WINDOW_WIDTH, WINDOW_HEIGHT)

class SnakeGame(Widget):
    score = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.snake = [(5, 5)]  # Initialer Körper der Schlange (Liste von Koordinaten)
        self.snake_dir = (1, 0)  # Richtung (x, y)
        self.food = (0, 0)  # Position des Essens
        self.generate_food()
        self.game_over = False
        self.label = Label(text="", font_size='24sp', bold=True, color=(1, 0, 0, 1), size_hint=(None, None),
                           pos=(WINDOW_WIDTH / 2 - 100, WINDOW_HEIGHT / 2 - 50))
        self.add_widget(self.label)
        Clock.schedule_interval(self.update, 0.2)
        Window.bind(on_key_down=self.on_key_down)

    def generate_food(self):
        while True:
            x = random.randint(0, (WINDOW_WIDTH // GRID_SIZE) - 1)
            y = random.randint(0, (WINDOW_HEIGHT // GRID_SIZE) - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def on_key_down(self, window, key, *args):
        dx, dy = self.snake_dir
        if key == 273 and dy == 0:  # Pfeil nach oben
            self.snake_dir = (0, 1)
        elif key == 274 and dy == 0:  # Pfeil nach unten
            self.snake_dir = (0, -1)
        elif key == 275 and dx == 0:  # Pfeil nach rechts
            self.snake_dir = (1, 0)
        elif key == 276 and dx == 0:  # Pfeil nach links
            self.snake_dir = (-1, 0)
        elif key == 32 and self.game_over:  # Leertaste zum Neustarten
            self.reset_game()

    def update(self, dt):
        if self.game_over:
            return

        # Bewege die Schlange
        head_x, head_y = self.snake[-1]
        dir_x, dir_y = self.snake_dir
        new_head = (head_x + dir_x, head_y + dir_y)

        # Kollisionsprüfung
        if (new_head in self.snake or
            not (0 <= new_head[0] < WINDOW_WIDTH // GRID_SIZE) or
            not (0 <= new_head[1] < WINDOW_HEIGHT // GRID_SIZE)):
            self.game_over = True
            self.label.text = f"Game Over! Score: {self.score}\nPress SPACE to restart."
            return

        self.snake.append(new_head)

        # Essen einsammeln
        if new_head == self.food:
            self.score += 1
            self.generate_food()
        else:
            self.snake.pop(0)

        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0, 1, 0)  # Grün für die Schlange
            for segment in self.snake:
                x, y = segment
                Rectangle(pos=(x * GRID_SIZE, y * GRID_SIZE), size=(GRID_SIZE, GRID_SIZE))

            Color(1, 0, 0)  # Rot für das Essen
            fx, fy = self.food
            Rectangle(pos=(fx * GRID_SIZE, fy * GRID_SIZE), size=(GRID_SIZE, GRID_SIZE))

    def reset_game(self):
        self.snake = [(5, 5)]
        self.snake_dir = (1, 0)
        self.food = (0, 0)
        self.score = 0
        self.game_over = False
        self.label.text = ""
        self.generate_food()

class SnakeApp(App):
    def build(self):
        game = SnakeGame()
        return game

if __name__ == "__main__":
    SnakeApp().run()
