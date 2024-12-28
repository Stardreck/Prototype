from kivy.uix.screenmanager import ScreenManager

from src.games.story_game import StoryGame
from src.star_engine import StarEngine


def main():
    # init kivy screen manager
    screen_manager = ScreenManager()
    # init game engine
    engine = StarEngine(screen_manager)
    # init default game
    game = StoryGame(engine)
    # start game loop
    game.run()

# entry point
if __name__ == "__main__":
    main()
