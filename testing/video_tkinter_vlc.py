import vlc
import tkinter as tk
from tkinter import messagebox

class VideoApp:
    def __init__(self, root, video_path):
        self.root = root
        self.root.title("Video Background Example")
        self.video_path = video_path

        # VLC Instance und Player Setup
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.media = self.instance.media_new(self.video_path)
        self.player.set_media(self.media)

        # Video-Frame für VLC
        self.video_frame = tk.Frame(root, bg="black")
        self.video_frame.pack(fill=tk.BOTH, expand=True)
        self.player.set_hwnd(self.video_frame.winfo_id())

        # Play das Video
        self.player.play()

        # Prüfen, ob das Video fertig ist
        self.check_video()

    def check_video(self):
        """Prüfe, ob das Video beendet ist."""
        if self.player.get_state() == vlc.State.Ended:
            self.player.stop()
            self.show_menu()
        else:
            self.root.after(100, self.check_video)

    def show_menu(self):
        """Zeige das Hauptmenü nach dem Video."""
        # Entferne das Video-Frame
        self.video_frame.destroy()

        # Hauptmenü-Ansicht
        label = tk.Label(self.root, text="Willkommen bei Stardreck!", font=("Arial", 24), fg="white", bg="black")
        label.pack(pady=50)

        button = tk.Button(self.root, text="Reise beginnen", font=("Arial", 16), bg="blue", fg="white", command=self.start_game)
        button.pack(pady=20)

    def start_game(self):
        """Logik für den Spielstart."""
        messagebox.showinfo("Spiel", "Das Spiel startet jetzt!")
        self.root.destroy()

# Hauptprogramm
if __name__ == "__main__":
    video_path = "../assets/test_video01.mp4"  # Ersetze durch den Pfad zu deinem Video
    root = tk.Tk()
    root.geometry("800x600")
    app = VideoApp(root, video_path)
    root.mainloop()
