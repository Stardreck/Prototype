from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class View(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        layout.add_widget(Label(text="Welcome to the Interactive Board Game!", font_size=24))
        layout.add_widget(Button(text="Start Game", size_hint=(1, 0.3), on_press=self.start_game))
        layout.add_widget(Button(text="Instructions", size_hint=(1, 0.3), on_press=self.show_instructions))
        layout.add_widget(Button(text="Exit", size_hint=(1, 0.3), on_press=self.exit_game))
        self.add_widget(layout)

    def start_game(self):
        pass

    def show_instructions(self):
        pass

    def exit_game(self):
        pass