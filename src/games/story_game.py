from typing import Dict, List, cast

import pygame

from components.ui.buttons.button import Button
from components.ui.image import Image
from components.ui.multiline_text import MultiLineText
from components.ui.panel import Panel
from components.ui.text import Text
from enums.button_state import ButtonState
from enums.color import Color
from games.game import Game
from games.game_data import GameData
from managers.debug_manager import DebugManager
from managers.event_manager import EventManager
from managers.input_manager import InputManager
from managers.inventory_manager import InventoryManager
from managers.quiz_manager import QuizManager
from managers.ui_manager import UIManager
from models.planet import Planet
from star_engine import StarEngine


class StoryGame(Game):
    def __init__(self, engine: StarEngine, data: GameData):
        super().__init__()
        self.engine = engine
        self.screen = engine.screen

        ##### Debug Manager #####
        self.debug_manager: DebugManager = DebugManager()

        ##### Input Manager #####
        self.input_manager: InputManager = InputManager(self)

        ##### UI Manager #####
        self.ui_manager: UIManager = UIManager(self)

        ##### Quiz Manager #####
        self.quiz_manager: QuizManager = QuizManager(self)

        ##### Event Manager #####
        self.event_manager: EventManager = EventManager(self, data.event_cards, data.event_probability)

        ##### Inventory Manager #####
        self.inventory_manager = InventoryManager(self)
        # debug
        self.inventory_manager.add_item(data.game_objects[0])

        ##### Game Data #####
        self.data = data
        self.fuel: int = 50
        self.hull: int = 50
        # Starting location
        self.player_row: int = 2
        self.player_col: int = 2
        self.current_planet = None
        self.planet_quizzes_current: Dict[str, List[dict]] = {
            pname: list(q_list) for pname, q_list in self.data.planet_quizzes.items()
        }

        ##### windows #####
        self.debug_rect: pygame.Rect = pygame.Rect(0, 0, engine.width // 2, engine.height)
        self.game_rect: pygame.Rect = pygame.Rect(engine.width // 2, 0, engine.width // 2, engine.height)

        self.default_bg_full: pygame.Surface | None = None
        self.default_bg_half: pygame.Surface | None = None
        self.planet_bg_full: Dict[str, pygame.Surface] = {}
        self.planet_bg_half: Dict[str, pygame.Surface] = {}

        self.load_backgrounds()

        ##### inventory #####
        self.is_inventory_open: bool = False
        self.sidebar_close_button_state: ButtonState = ButtonState.IDLE

        ##### states #####
        self.is_planet_menu_present = False
        self.is_planet_station_menu_present = False

    def load_backgrounds(self):
        try:
            img = pygame.image.load("assets/welcome_screen.png").convert()
        except:
            img = pygame.Surface((self.engine.width, self.engine.height))
            img.fill(Color.GAME_BG.value)

        self.default_bg_full = pygame.transform.scale(img, (self.engine.width, self.engine.height))
        half_w = self.engine.width // 2
        half_h = self.engine.height
        self.default_bg_half = pygame.transform.scale(img, (half_w, half_h))

        for planet in self.data.planets:
            if not planet.background_image:
                continue
            try:
                p_img = pygame.image.load(planet.background_image).convert()
            except:
                p_img = pygame.Surface((self.engine.width, self.engine.height))
                p_img.fill((80, 0, 0))

            bg_full = pygame.transform.scale(p_img, (self.engine.width, self.engine.height))
            bg_half = pygame.transform.scale(p_img, (half_w, half_h))
            self.planet_bg_full[planet.name] = bg_full
            self.planet_bg_half[planet.name] = bg_half

    def handle_events(self):
        self.input_manager.process_events()

    def update(self, dt: float):
        pass

    def draw(self):
        # if the player is on a planet, get the current planet name
        planet_name = self.current_planet.name if self.current_planet else None

        if self.debug_manager.debug_mode:
            # display debug view (50%)
            debug_surface = self.screen.subsurface(self.debug_rect)
            self.debug_manager.draw_debug(debug_surface, self)
            # display game view (50%)
            game_surface = self.screen.subsurface(self.game_rect)
            if planet_name and planet_name in self.planet_bg_half:
                game_surface.blit(self.planet_bg_half[planet_name], (0, 0))
            else:
                game_surface.blit(self.default_bg_half, (0, 0))
            self.ui_manager.draw_hud(game_surface)
        else:
            if planet_name and planet_name in self.planet_bg_full:
                # display planet view (100%)
                self.screen.blit(self.planet_bg_full[planet_name], (0, 0))
            else:
                # display default solar system view (100%)
                self.screen.blit(self.default_bg_full, (0, 0))
            self.ui_manager.draw_hud(self.screen)

    def handle_movement(self, event: pygame.event.Event):
        move_row, move_column = 0, 0
        if event.key == pygame.K_UP:
            move_row = -1
        elif event.key == pygame.K_DOWN:
            move_row = 1
        elif event.key == pygame.K_LEFT:
            move_column = -1
        elif event.key == pygame.K_RIGHT:
            move_column = 1

        if (move_row != 0 or move_column != 0) and self.fuel > 0:
            self.player_row += move_row
            self.player_col += move_column
            self.fuel -= 1
            self.check_planet_visit()
        elif (move_row != 0 or move_column != 0):
            self.game_over("Kein Treibstoff mehr!")

    def handle_touch_mouse_down(self, event: pygame.event.Event):
        mouse_pos = event.pos
        # Toggle inventory visibility when clicking the sidebar icon
        if self.ui_manager.hud.inventory_button_rect.collidepoint(mouse_pos):
            self.is_inventory_open = not self.is_inventory_open

        # Set close button state to clicked while pressed
        elif self.is_inventory_open and self.ui_manager.hud.close_button_rect.collidepoint(mouse_pos):
            self.sidebar_close_button_state = ButtonState.CLICKED

    def handle_touch_mouse_up(self, event: pygame.event.Event):
        # close button released, close inventory
        if self.ui_manager.hud.close_button_rect.collidepoint(event.pos) and self.is_inventory_open:
            self.is_inventory_open = False
            self.sidebar_close_button_state = ButtonState.IDLE

    def handle_touch_mouse_motion(self, event: pygame.event.Event):
        # mouse is hovering over the close button
        if self.ui_manager.hud.close_button_rect.collidepoint(event.pos) and self.is_inventory_open:
            self.sidebar_close_button_state = ButtonState.HOVER
        else:
            self.sidebar_close_button_state = ButtonState.IDLE

    def check_planet_visit(self):
        self.current_planet = None
        found_planet = False

        # loop through each planet object
        for planet in self.data.planets:
            # check if the planet coordinates matches the player ones
            if planet.row == self.player_row and planet.col == self.player_col:
                self.current_planet = planet
                found_planet = True
                if not planet.visited:
                    planet.visited = True
                    self.trigger_planet_event(planet)
                break

        ##### events #####
        executed_forced_card = self.event_manager.check_for_forced_events()
        if executed_forced_card:
            if executed_forced_card.category == "game_over":
                self.game_over(executed_forced_card.description)
                return

        if self.event_manager.should_trigger_event():
            self.event_manager.trigger_random_event()

        ##### quizzes #####
        if not found_planet:
            quiz_data = self.quiz_manager.get_random_quiz_for_planet("default")
            if quiz_data:
                self.quiz_manager.run_quiz_scene(quiz_data)

    def trigger_planet_event(self, planet):
        if planet.name in self.data.story_segments:
            ##### display planet menu #####
            self.run_planet_menu_loop(planet)

    def run_planet_menu_loop(self, planet: Planet):
        self.is_planet_menu_present = True

        # visit station
        first_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_first_button"))
        first_button.set_on_click(lambda: self.run_planet_station_loop(planet))

        # visit planet
        second_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_second_button"))
        second_button.set_on_click(lambda: self.render_planet_story(planet))

        while self.is_planet_menu_present  and self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                        return
                    elif event.key == pygame.K_d:
                        self.debug_manager.toggle_debug_mode()
                for key, component in self.ui_manager.ui_components.items():
                    component.handle_event(event)

            self.draw()

            self.render_planet_menu_overlay(planet)

        # reset callback
        first_button.set_on_click(None)
        second_button.set_on_click(None)

    def run_planet_station_loop(self, planet: Planet):
        self.is_planet_menu_present = False
        self.is_planet_station_menu_present = True

        # solve quiz
        first_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_first_button"))
        first_button.set_on_click(lambda: self.handle_planet_station_choice(planet, 1))

        # get free fuel
        second_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_second_button"))
        second_button.set_on_click(lambda: self.handle_planet_station_choice(planet, 2))

        while self.is_planet_station_menu_present  and self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.stop()
                        return
                    elif event.key == pygame.K_d:
                        self.debug_manager.toggle_debug_mode()
                for key, component in self.ui_manager.ui_components.items():
                    component.handle_event(event)

            self.draw()

            self.render_planet_station_overlay(planet)

        # reset callback
        first_button.set_on_click(None)
        second_button.set_on_click(None)

    def handle_planet_station_choice(self, planet: Planet, choice: int):
        """
        Handle the player's selection at the planet station.

        If choice == 1, present a quiz (or task) to the player. If the player answers
        correctly, add +10 fuel and display a message indicating success. If the answer
        is wrong, add +3 fuel and display a message indicating the incorrect answer but reward.

        If choice == 2, no challenge is presented and the player receives +5 fuel along with
        a message stating that the ship has been refueled.

        Afterwards, the planet menu is shown again.
        """
        message = ""
        if choice == 1:
            # Present a quiz or task challenge
            # Try to get a quiz designated for the station challenge.
            quiz_data = self.quiz_manager.get_random_quiz_for_planet("default")
            # Run the quiz scene. We assume that after the quiz is finished,
            # the quiz manager sets an attribute 'last_result' (True if correct, False if wrong).
            self.quiz_manager.run_quiz_scene(quiz_data)


            # Check the result of the quiz challenge
            if self.quiz_manager.last_result_is_correct:
                self.fuel += 10
                message = "Correct! You have received +10 fuel."
                self.quiz_manager.last_result_is_correct = False
            else:
                self.fuel += 3
                message = "Incorrect! You still receive +3 fuel."
        elif choice == 2:
            # No challenge; simply add +5 fuel
            self.fuel += 5
            message = "The ship has been refueled: +5 fuel received."

        self.is_planet_station_menu_present = False

        # Display the overlay message using the new UI method.
        self.ui_manager.display_message_overlay(message)

        # After handling the station choice, return to the planet menu overlay.
        self.run_planet_menu_loop(planet)

    def handle_planet_station_choicex(self, planet: Planet, choice: int):
        # todo implement logic
        # solve quiz
        if choice == 1:
            # display a quiz or task, if quiz or task is solved correctly add fuel + 10, if not add fuel +3
            # display message that shows the added fuel and if solved correctly or wrongly
            pass
        # get free fuel
        if choice == 2:
            # display message that the ship has been refueled with +5
            self.fuel += 5
            pass


    def render_planet_menu_overlay(self, planet: Planet):
        target_surface = (self.screen.subsurface(self.game_rect)
                          if self.debug_manager.debug_mode else self.screen)

        bg_panel = cast(Panel, self.ui_manager.ui_components.get("choice_panel_bg"))
        bg_panel.draw(target_surface)

        panel = cast(Panel, self.ui_manager.ui_components.get("choice_panel"))
        panel.draw(target_surface)

        title = cast(Text, self.ui_manager.ui_components.get("choice_panel_title"))
        title.set_text(planet.name)
        title.draw(target_surface)

        description = cast(MultiLineText, self.ui_manager.ui_components.get("choice_panel_description"))
        description.set_text(planet.description)
        description.draw(target_surface)

        image = cast(Image, self.ui_manager.ui_components.get("choice_panel_image"))
        image.set_image_path(planet.background_image)
        image.draw(target_surface)

        first_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_first_button"))
        first_button.draw(target_surface)
        first_button.set_text("Handelstation besuchen")

        second_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_second_button"))
        second_button.draw(target_surface)
        second_button.set_text("Planet besuchen")

        pygame.display.flip()

    def render_planet_station_overlay(self, planet: Planet):
        self.is_planet_menu_present = False
        target_surface = (self.screen.subsurface(self.game_rect)
                          if self.debug_manager.debug_mode else self.screen)

        bg_panel = cast(Panel, self.ui_manager.ui_components.get("choice_panel_bg"))
        bg_panel.draw(target_surface)

        panel = cast(Panel, self.ui_manager.ui_components.get("choice_panel"))
        panel.draw(target_surface)

        title = cast(Text, self.ui_manager.ui_components.get("choice_panel_title"))
        title.set_text(f"{planet.name} - Handelsstation")
        title.draw(target_surface)

        description = cast(MultiLineText, self.ui_manager.ui_components.get("choice_panel_description"))
        description.set_text("Dies ist eine hardcoded Beschreibung einer Handelsstation")
        description.draw(target_surface)

        image = cast(Image, self.ui_manager.ui_components.get("choice_panel_image"))
        image.set_image_path(planet.background_image)
        image.draw(target_surface)

        first_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_first_button"))
        first_button.draw(target_surface)
        first_button.set_text("Aufgabe lösen")

        second_button = cast(Button, self.ui_manager.ui_components.get("choice_panel_second_button"))
        second_button.draw(target_surface)
        second_button.set_text("Kostenlos tanken")

        pygame.display.flip()

    def render_planet_story(self, planet: Planet):
        self.is_planet_menu_present = False
        if planet.cutscene_media:
            self.ui_manager.display_cutscene(planet.cutscene_media)

        story = self.data.story_segments[planet.name]
        for line in story.story_lines:
            self.ui_manager.display_text_blocking(line)

    def trigger_planet_eventX(self, planet):
        if planet.name in self.data.story_segments:
            ##### display planet options menu #####
            prompt = f"Sie haben den Planeten {planet.name} erreicht. Was möchten Sie tun?"
            options = ["Planet besuchen", "Im Orbit bleiben und zur Handelsstation gehen", "test1", "test2", "test3"]
            choice = self.ui_manager.display_multiple_choice(prompt, options)
            ##### choice overview #####
            # 0 = visit planet
            # 1 = stay in orbit (fuel station)
            if choice == 0:

                self.ui_manager.display_cutscene(planet.cutscene_media)

                story = self.data.story_segments[planet.name]
                for line in story.story_lines:
                    self.ui_manager.display_text_blocking(line)

            elif choice == 1:
                pass

        # Planetenspezifisches Quiz
        quiz_data = self.quiz_manager.get_random_quiz_for_planet(planet.name)
        if quiz_data:
            self.quiz_manager.run_quiz_scene(quiz_data)

        if planet.is_fuel_planet:
            self.fuel += 5
            self.ui_manager.display_text_blocking("Ihr habt +5 Fuel gefunden!")

    def game_over(self, reason: str):
        print("GAME OVER:", reason)
        self.ui_manager.display_text_blocking(f"GAME OVER: {reason}")
        self.stop()
