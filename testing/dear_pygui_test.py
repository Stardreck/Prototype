# Dear PyGui Implementation
from dearpygui import *
from dearpygui import *

def dear_pygui_menu():
    def start_button_callback(sender, data):
        print("Game Started!")

    set_main_window_size(800, 600)
    set_main_window_title("Sci-Fi Start Menu - Dear PyGui")

    with window("Start Menu", width=800, height=600):
        add_text("Welcome to the Sci-Fi World", color=[0, 255, 255])
        add_spacing(count=5)
        add_button("Start", callback=start_button_callback, width=100, height=50)

    start_dearpygui()

# Run the menus for comparison
if __name__ == "__main__":
    print("1: Pygame GUI Menu")
    print("2: Dear PyGui Menu")
    choice = input("Enter your choice (1/2): ")

    if choice == "1":
        pygame_gui_menu()
    elif choice == "2":
        dear_pygui_menu()
    else:
        print("Invalid choice")
