import vlc
import time

def play_video(video_path):
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(video_path)
    player.set_media(media)

    print("Starte das Video...")
    player.play()

    time.sleep(1)  # Warte, bis das Video startet

    if player.is_playing():
        print("Das Video wird abgespielt.")
    else:
        print("Das Video konnte nicht abgespielt werden.")

    while player.is_playing():
        time.sleep(1)

if __name__ == "__main__":
    play_video("assets/test_video02.mp4")
