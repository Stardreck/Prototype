from src.star_engine import StarEngine
from src.games.story_game import StoryGame
def main():
    # init game engine
    engine = StarEngine()
    # init default game
    game = StoryGame(engine)
    # start game loop
    game.run()

# entry point
if __name__ == "__main__":
    main()
