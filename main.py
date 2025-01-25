from games.story.game_data import GameData
from games.story.story_game import StoryGame
from plugins.video_player import VideoPlayer
from star_engine import StarEngine


def main():
    ##### intro video #####
    player = VideoPlayer(None)
    player.enable_standalone(1600, 720, "StarDreck")
    player.set_video("assets/test_video01.mp4")
    player.play()


    ##### init game engine #####
    engine = StarEngine()
    ##### show main menu #####
    result = engine.show_main_menu()
    if result == "quit":
        return
    if result == "storygame":
        data = GameData()
        game = StoryGame(engine, data)
        engine.run(game)



# entry point
if __name__ == "__main__":
    main()
