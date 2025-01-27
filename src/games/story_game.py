from typing import Dict, List

import pygame

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
        if self.event_manager.should_trigger_event():
            self.event_manager.trigger_random_event()

        ##### quizzes #####
        if not found_planet:
            quiz_data = self.quiz_manager.get_random_quiz_for_planet("default")
            if quiz_data:
                self.quiz_manager.run_quiz_scene(quiz_data)

    def trigger_planet_event(self, planet):
        if planet.name in self.data.story_segments:
            ##### display planet options menu #####
            prompt = f"Sie haben den Planeten {planet.name} erreicht. Was möchten Sie tun?"
            options = ["Planet besuchen", "Im Orbit bleiben und zur Handelsstation gehen"]
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
