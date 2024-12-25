import pyglet
from pyglet.window import key, mouse
from pyglet.text import Label
from pyglet.shapes import Rectangle

class InteractiveBoardGame:
    def __init__(self):
        # Initialize the game window
        self.window = pyglet.window.Window(width=800, height=600, caption="Interactive Board Game")
        self.window.push_handlers(self)

        # Scene manager and state tracking
        self.scenes = {}
        self.current_scene = None
        self.stats = {
            "score": 0,
            "failed_questions": []
        }
        self.quiz_stats = {
            "Physics - Dynamics": [],
            "Physics - Thermodynamics": [],
            "Physics - Astronomy": []
        }
        self.story_state = {}

        # Load assets (placeholder)
        self.load_assets()

    def load_assets(self):
        # Placeholder for loading images, videos, and sounds
        self.assets = {}

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, name):
        if name in self.scenes:
            self.current_scene = self.scenes[name]
            self.current_scene.start()
        else:
            print(f"Scene '{name}' not found.")

    def on_draw(self):
        self.window.clear()
        if self.current_scene:
            self.current_scene.draw()

    def on_key_press(self, symbol, modifiers):
        if self.current_scene:
            self.current_scene.handle_key(symbol)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_scene and button == mouse.LEFT:
            self.current_scene.handle_mouse_click()

    def run(self):
        pyglet.app.run()

class Scene:
    def __init__(self, game):
        self.game = game
        self.next_scene = None
        self.alternate_scene_conditions = []

    def set_next_scene(self, next_scene):
        self.next_scene = next_scene

    def add_alternate_scene(self, condition, scene_name):
        self.alternate_scene_conditions.append((condition, scene_name))

    def determine_next_scene(self):
        for condition, scene_name in self.alternate_scene_conditions:
            if condition(self.game):
                return scene_name
        return self.next_scene

    def start(self):
        pass

    def draw(self):
        pass

    def handle_key(self, symbol):
        next_scene = self.determine_next_scene()
        if symbol == key.RETURN and next_scene:
            self.game.set_scene(next_scene)

    def handle_mouse_click(self):
        next_scene = self.determine_next_scene()
        if next_scene:
            self.game.set_scene(next_scene)

class StoryScene(Scene):
    def __init__(self, game, text, background):
        super().__init__(game)
        self.text = text
        self.background = pyglet.image.load(background)
        self.black_bar = Rectangle(0, 0, self.game.window.width, 100, color=(0, 0, 0, 102))  # 0.4 transparency
        self.displayed_text = ""
        self.char_index = 0
        self.speed = 0.05  # Speed for animating text
        self.label = Label(self.displayed_text, x=20, y=20, multiline=True, width=760, color=(255, 255, 255, 255))

    def start(self):
        self.displayed_text = ""
        self.char_index = 0
        pyglet.clock.schedule_interval(self.animate_text, self.speed)

    def draw(self):
        self.background.blit(0, 0)
        self.black_bar.draw()
        self.label.draw()

    def animate_text(self, dt):
        if self.char_index < len(self.text):
            self.char_index += 1
            self.displayed_text = self.text[:self.char_index]
            self.label.text = self.displayed_text
        else:
            pyglet.clock.unschedule(self.animate_text)

class QuizScene(Scene):
    def __init__(self, game, question, options, correct_option, explanation_scene, topic):
        super().__init__(game)
        self.question = question
        self.options = options
        self.correct_option = correct_option
        self.explanation_scene = explanation_scene
        self.topic = topic
        self.label = Label(self.question, x=50, y=300, width=700, multiline=True, color=(255, 255, 255, 255))
        self.option_labels = [
            Label(f"{i + 1}. {opt}", x=50, y=250 - i * 30, color=(255, 255, 255, 255))
            for i, opt in enumerate(options)
        ]

    def draw(self):
        self.label.draw()
        for option_label in self.option_labels:
            option_label.draw()

    def handle_key(self, symbol):
        if symbol in (key._1, key._2, key._3, key._4):
            selected = symbol - key._1 + 1
            if selected == self.correct_option:
                self.game.stats["score"] += 1
                print("Correct Answer!")
                next_scene = self.determine_next_scene()
                if next_scene:
                    self.game.set_scene(next_scene)
            else:
                self.game.stats["failed_questions"].append(self.question)
                self.game.quiz_stats[self.topic].append({"question": self.question, "correct": False})
                if len(self.game.stats["failed_questions"]) >= 3:
                    self.game.set_scene("alternate_story")
                else:
                    self.game.set_scene(self.explanation_scene)
            if selected == self.correct_option:
                self.game.quiz_stats[self.topic].append({"question": self.question, "correct": True})

class ExplanationScene(Scene):
    def __init__(self, game, explanation, background):
        super().__init__(game)
        self.explanation = explanation
        self.background = pyglet.image.load(background)
        self.label = Label(self.explanation, x=50, y=150, width=700, multiline=True, color=(255, 255, 255, 255))

    def draw(self):
        self.background.blit(0, 0)
        self.label.draw()

class StatsScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.label = Label("", x=50, y=300, width=700, multiline=True, color=(255, 255, 255, 255))

    def start(self):
        stats_text = "Quiz Performance:\n"
        for topic, results in self.game.quiz_stats.items():
            stats_text += f"{topic}:\n"
            for result in results:
                stats_text += f"  Question: {result['question']} - {'Correct' if result['correct'] else 'Wrong'}\n"
        self.label.text = stats_text

    def draw(self):
        self.label.draw()

if __name__ == "__main__":
    game = InteractiveBoardGame()

    # Creating story scenes
    story_scene1 = StoryScene(game, "Welcome to the Adventure!", "./assets/welcome_screen.jpeg")
    story_scene2 = StoryScene(game, "You are now entering the quiz!", "./assets/welcome_screen.jpeg")
    story_scene3 = StoryScene(game, "Congratulations on progressing further!", "./assets/welcome_screen.jpeg")
    story_scene4 = StoryScene(game, "The journey takes an unexpected turn!", "./assets/welcome_screen.jpeg")
    story_scene5 = StoryScene(game, "You discover a hidden truth!", "./assets/welcome_screen.jpeg")
    story_scene6 = StoryScene(game, "A new challenge awaits!", "./assets/welcome_screen.jpeg")

    # Creating quiz scenes
    quiz_scene1 = QuizScene(
        game, "What is 2 + 2?", ["1", "2", "3", "4"], 4, "explanation1", "Physics - Dynamics"
    )
    quiz_scene2 = QuizScene(
        game, "What is the capital of France?", ["Berlin", "Madrid", "Paris", "Rome"], 3, "explanation2", "Physics - Thermodynamics"
    )
    quiz_scene3 = QuizScene(
        game, "What is the largest planet?", ["Earth", "Mars", "Jupiter", "Venus"], 3, "explanation3", "Physics - Astronomy"
    )

    # Creating explanation scenes
    explanation_scene1 = ExplanationScene(game, "The correct answer is 4 because 2 + 2 equals 4.", "./assets/welcome_screen.jpeg")
    explanation_scene2 = ExplanationScene(game, "The correct answer is Paris, the capital of France.", "./assets/welcome_screen.jpeg")
    explanation_scene3 = ExplanationScene(game, "The correct answer is Jupiter, the largest planet.", "./assets/welcome_screen.jpeg")

    # Creating alternate story scene
    alternate_story = StoryScene(game, "The alternate story begins here due to failed quizzes.", "./assets/welcome_screen.jpeg")

    # Creating stats scene
    stats_scene = StatsScene(game)

    # Linking scenes dynamically
    story_scene1.set_next_scene("story2")
    story_scene2.set_next_scene("quiz1")
    quiz_scene1.set_next_scene("story3")
    quiz_scene2.set_next_scene("story4")
    quiz_scene3.set_next_scene("story5")
    explanation_scene1.set_next_scene("story3")
    explanation_scene2.set_next_scene("story4")
    explanation_scene3.set_next_scene("story5")
    story_scene3.set_next_scene("quiz2")
    story_scene4.set_next_scene("quiz3")
    story_scene5.set_next_scene("stats")

    # Adding alternate story conditions
    story_scene1.add_alternate_scene(lambda g: len(g.stats["failed_questions"]) >= 3, "alternate_story")

    # Adding scenes to the game
    game.add_scene("story1", story_scene1)
    game.add_scene("story2", story_scene2)
    game.add_scene("story3", story_scene3)
    game.add_scene("story4", story_scene4)
    game.add_scene("story5", story_scene5)
    game.add_scene("story6", story_scene6)
    game.add_scene("quiz1", quiz_scene1)
    game.add_scene("quiz2", quiz_scene2)
    game.add_scene("quiz3", quiz_scene3)
    game.add_scene("explanation1", explanation_scene1)
    game.add_scene("explanation2", explanation_scene2)
    game.add_scene("explanation3", explanation_scene3)
    game.add_scene("alternate_story", alternate_story)
    game.add_scene("stats", stats_scene)

    game.set_scene("story1")
    game.run()