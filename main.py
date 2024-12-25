from src.games.story_game import StoryGame
from src.star_engine import StarEngine


def main():
    print("Hello World!")
    engine = StarEngine()
    game = StoryGame(engine)
    game.run()

if __name__ == "__main__":
    main()


