from typing import Dict, List

import pygame

from enums.color import Color
from games.game import Game
from games.game_data import GameData
from managers.debug_manager import DebugManager
from managers.event_manager import EventManager
from managers.input_manager import InputManager
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

        ##### Event Manager #####
        self.event_manager: EventManager = EventManager(self, data.event_cards, data.event_probability)

        ##### Input Manager #####
        self.input_manager: InputManager = InputManager(self)

        ##### UI Manager #####
        self.ui_manager: UIManager = UIManager(self)

        ##### Quiz Manager #####
        self.quiz_manager: QuizManager = QuizManager(self)

        ##### Game Data #####
        self.data = data
        self.fuel: int = 50
        self.hull: int = 50
        # Starting location
        self.player_row: int = 1
        self.player_col: int = 5
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
            if not planet.bg_image:
                continue
            try:
                p_img = pygame.image.load(planet.bg_image).convert()
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
            self.trigger_random_event()

        ##### quizzes #####
        if not found_planet:
            quiz_data = self.quiz_manager.get_random_quiz_for_planet("default")
            if quiz_data:
                self.quiz_manager.run_quiz_scene(quiz_data)

    def trigger_planet_event(self, planet):
        if planet.name in self.data.story_segments:
            for line in self.data.story_segments[planet.name].lines:
                self.ui_manager.display_text_blocking(line)

        # Planetenspezifisches Quiz
        quiz_data = self.quiz_manager.get_random_quiz_for_planet(planet.name)
        if quiz_data:
            self.quiz_manager.run_quiz_scene(quiz_data)

        if planet.is_fuel_planet:
            self.fuel += 5
            self.ui_manager.display_text_blocking("Ihr habt +5 Fuel gefunden!")

    def trigger_random_event(self):
        card = self.event_manager.pick_event()
        if not card:
            return
        self.event_manager.apply_event_scaling(card)
        # => Animiertes Darstellen
        self.event_manager.display_event_card_animated(card)

        self.fuel += card.fuel_change
        self.hull += card.hull_change
        if self.hull <= 0:
            self.game_over("Hull <= 0. Zerstört!")

    ###########################################################################
    # todo methods not tested
    ###########################################################################
    def run_quiz_multiple_choice(self, quiz_data):
        question = quiz_data["question"]
        options = quiz_data["options"]
        correct_idx = quiz_data["correct_idx"]

        typed_input = ""
        font = pygame.font.SysFont(None, 24)
        waiting = True

        while waiting and self.is_running:
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
                    elif event.key == pygame.K_RETURN:
                        if typed_input.isdigit():
                            if int(typed_input) == correct_idx:
                                self.ui_manager.display_text_blocking("Richtig beantwortet!")
                                self.event_manager.decrease_error_count()
                            else:
                                self.ui_manager.display_text_blocking("Falsch! Hull -1.")
                                self.hull -= 1
                                self.event_manager.increase_error_count()
                                if self.hull <= 0:
                                    self.game_over("Euer Schiff ist zerstört!")
                            waiting = False
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        typed_input = typed_input[:-1]
                    elif event.key in range(pygame.K_0, pygame.K_9 + 1):
                        typed_input += str(event.key - pygame.K_0)

            self.draw()

            target_surf = self.screen.subsurface(self.game_rect) if self.debug_manager.debug_mode else self.screen
            ow_w = target_surf.get_width()
            ow_h = 250

            overlay_rect = pygame.Rect(0, target_surf.get_height() - ow_h, ow_w, ow_h)
            quiz_overlay = pygame.Surface((ow_w, ow_h))
            quiz_overlay.set_alpha(180)
            quiz_overlay.fill(Color.BLACK.value)

            lines = [f"QUIZ: {question}"]
            for i, opt in enumerate(options):
                lines.append(f"{i}) {opt}")
            lines.append("")
            lines.append(f"Antwort eingeben (0-{len(options) - 1}): {typed_input}")

            y_off = 10
            for line in lines:
                line_img = font.render(line, True, Color.WHITE.value)
                quiz_overlay.blit(line_img, (10, y_off))
                y_off += line_img.get_height() + 5

            target_surf.blit(quiz_overlay, (overlay_rect.x, overlay_rect.y))
            pygame.display.flip()

    def run_quiz_task(self, quiz_data):
        question = quiz_data["question"]
        correct_value = quiz_data["correct_value"]

        typed_input = ""
        font = pygame.font.SysFont(None, 24)
        waiting = True

        while waiting and self.is_running:
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
                    elif event.key == pygame.K_RETURN:
                        try:
                            user_val = float(typed_input)
                            tolerance = abs(correct_value * 0.01)
                            if abs(user_val - correct_value) <= tolerance:
                                self.ui_manager.display_text_blocking("Richtig beantwortet!")
                                self.event_manager.decrease_error_count()
                            else:
                                self.ui_manager.display_text_blocking("Falsch! Hull -1.")
                                self.hull -= 1
                                self.event_manager.increase_error_count()
                                if self.hull <= 0:
                                    self.game_over("Euer Schiff ist zerstört!")
                            waiting = False
                            return
                        except ValueError:
                            pass
                    elif event.key == pygame.K_BACKSPACE:
                        typed_input = typed_input[:-1]
                    elif (event.key >= pygame.K_0 and event.key <= pygame.K_9) or event.key == pygame.K_PERIOD:
                        char = "." if event.key == pygame.K_PERIOD else str(event.key - pygame.K_0)
                        typed_input += char

            self.draw()

            target_surf = self.screen.subsurface(self.game_rect) if self.debug_manager.debug_mode else self.screen
            ow_w = target_surf.get_width()
            ow_h = 250

            overlay_rect = pygame.Rect(0, target_surf.get_height() - ow_h, ow_w, ow_h)
            quiz_overlay = pygame.Surface((ow_w, ow_h))
            quiz_overlay.set_alpha(180)
            quiz_overlay.fill(Color.BLACK.value)

            lines = [f"AUFGABE: {question}"]
            lines.append("")
            lines.append(f"Zahl eingeben: {typed_input}")

            y_off = 10
            for line in lines:
                line_img = font.render(line, True, Color.WHITE.value)
                quiz_overlay.blit(line_img, (10, y_off))
                y_off += line_img.get_height() + 5

            target_surf.blit(quiz_overlay, (overlay_rect.x, overlay_rect.y))
            pygame.display.flip()

    ###########################################################################
    # HELPER METHODS
    ###########################################################################
    def game_over(self, reason: str):
        print("GAME OVER:", reason)
        self.ui_manager.display_text_blocking(f"GAME OVER: {reason}")
        self.stop()
