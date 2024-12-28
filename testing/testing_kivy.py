from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.core.window import Window


class StarEngine:
    def __init__(self, screen_manager):
        self.screen_manager = screen_manager

    def add_screen(self, screen):
        self.screen_manager.add_widget(screen)

    def set_screen(self, screen_name):
        self.screen_manager.current = screen_name


class VideoPlayerScreen(Screen):
    def __init__(self, engine, video_source, next_screen, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.video_source = video_source
        self.next_screen = next_screen

        # Video without controls
        self.video = Video(source=self.video_source)
        self.video.state = "play"
        self.add_widget(self.video)

        # Check video status
        Clock.schedule_interval(self.check_video_status, 0.5)

        # Bind key events to skip video
        Window.bind(on_key_down=self.skip_video)

    def check_video_status(self, dt):
        if self.video.state == "stop":
            self.goto_next_screen()

    def skip_video(self, *args):
        self.goto_next_screen()

    def goto_next_screen(self):
        self.video.state = "stop"
        self.remove_widget(self.video)
        self.engine.set_screen(self.next_screen)
        Clock.unschedule(self.check_video_status)
        Window.unbind(on_key_down=self.skip_video)


class MainMenuScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Welcome to the Interactive Board Game!", font_size=24))
        layout.add_widget(Button(text="Start Game", size_hint=(1, 0.3), on_press=self.start_game))
        layout.add_widget(Button(text="Instructions", size_hint=(1, 0.3), on_press=self.show_instructions))
        layout.add_widget(Button(text="Exit", size_hint=(1, 0.3), on_press=self.exit_game))

        self.add_widget(layout)

    def start_game(self, instance):
        self.engine.set_screen('game')

    def show_instructions(self, instance):
        popup = Popup(title="Instructions",
                      content=Label(text="Complete the physics tasks to progress through the game!"),
                      size_hint=(0.8, 0.6))
        popup.open()

    def exit_game(self, instance):
        App.get_running_app().stop()


class GameScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine
        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.story_label = Label(text="Game Story Placeholder", font_size=18)
        self.task_label = Label(text="Solve the task to proceed!", font_size=16)
        self.answer_input = TextInput(hint_text="Enter your answer here", multiline=False)
        self.submit_button = Button(text="Submit", size_hint=(1, 0.3), on_press=self.check_answer)

        self.layout.add_widget(self.story_label)
        self.layout.add_widget(self.task_label)
        self.layout.add_widget(self.answer_input)
        self.layout.add_widget(self.submit_button)

        self.add_widget(self.layout)

    def check_answer(self, instance):
        user_answer = self.answer_input.text
        if user_answer == "correct":  # Placeholder logic for the correct answer
            self.story_label.text = "Correct! Moving to the next task."
        else:
            self.story_label.text = "Incorrect. Try again."


class StoryGame:
    def __init__(self, engine):
        self.engine = engine

    def run(self):
        app = InteractiveBoardGameApp(self.engine)
        app.run()

class InteractiveBoardGameApp(App):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

    def build(self):
        return self.engine.screen_manager


def main():
    # init kivy screen manager
    screen_manager = ScreenManager()
    # init game engine
    engine = StarEngine(screen_manager)

    # Add screens
    engine.add_screen(VideoPlayerScreen(engine, video_source="../assets/test_video01.mp4", next_screen="menu", name="intro"))
    engine.add_screen(MainMenuScreen(engine, name="menu"))
    engine.add_screen(GameScreen(engine, name="game"))

    # Start with intro screen
    engine.set_screen('intro')

    # init default game
    game = StoryGame(engine)
    # start game loop
    game.run()


# entry point
if __name__ == "__main__":
    main()
