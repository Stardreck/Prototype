import json

import pygame
from pygame.sprite import Group
import random
from data.data import PLANETS_DATA, STORY_TEXTS, TASKS_DATA, QUIZ_DATA, EVENT_CARDS, SHIP_INTERIOR_MAP, \
    EVENT_PROBABILITY
from data.settings import BLACK
from players.player import Player
from src.games.game import Game, MapState
from star_engine import StarEngine


class StoryGame(Game):
    def __init__(self, engine: StarEngine):
        super().__init__(engine)
        # load game data
        self.planets = PLANETS_DATA
        self.story_texts = STORY_TEXTS
        self.tasks_data = TASKS_DATA
        self.quiz_data = QUIZ_DATA
        self.event_cards = EVENT_CARDS
        self.ship_rooms = SHIP_INTERIOR_MAP

        self.fuel = 5
        self.hull = 5

        # Player
        self.player = Player(self.width, self.height)
        self.all_sprites = Group(self.player)

        self.reload_overlay_background()

    # self.stats = GameStats()

    def on_key_press(self, event):
        """
        Handles key press events. Called when a key is pressed.

        Args:
            event (pygame.event.Event): The key press event.
        """
        print(f"Key pressed: {event.key}")

        # L KEY pressed
        if event.key == pygame.K_l:
            self.debug_manager.toggle_debug_mode()
            self.debug_manager.create_surfaces(self)
            self.reload_overlay_background()

        if self.map_state == MapState.SYSTEM:
            self.handle_system_map_events(event)

    def handle_events(self):
        for event in pygame.event.get():

            # ESCAPE Key
            if event.type == pygame.QUIT:
                self.on_quit()

            # KEY pressed
            elif event.type == pygame.KEYDOWN:
                self.on_key_press(event)

    def update(self):
        pass

    def draw(self):

        self.screen.fill(BLACK)
        if self.debug_manager.is_debug_active():
            if self.game_state=="system_map":
                self.debug_manager.draw_system_map_debug(self)
            #elif self.game_state=="ship_interior":
            #    self.debug_manager.draw_ship_interior_debug(self)
        else:
            if self.board_surface:
                self.board_surface.fill(BLACK)
        if self.game_state=="game_over":
            # self.draw_game_over()
            pass
        else:
            if self.overlay_surface and self.overlay_background:
                self.overlay_surface.blit(self.overlay_background,(0,0))

    def run(self):
        super().run()

    def reload_overlay_background(self):
        if self.overlay_surface:
            width = self.overlay_surface.get_width()
            height = self.overlay_surface.get_height()
            try:
                tmp = pygame.image.load("assets/welcome_screen.png")
                self.overlay_background = pygame.transform.scale(tmp, (width, height))
            except:
                pass

    # ***** MAP LOGIC *****
    def handle_system_map_events(self, event: pygame.event.Event):
        # player position, movement logic

        dx, dy = 0, 0
        if event.key == pygame.K_UP:
            dy = -1
        elif event.key == pygame.K_DOWN:
            dy = 1
        elif event.key == pygame.K_LEFT:
            dx = -1
        elif event.key == pygame.K_RIGHT:
            dx = 1
        elif event.key == pygame.K_p:
            # todo ship map
            # self.game_state="ship_interior"
            self.player.ship_x = 0
            self.player.ship_y = 0
            self.player.update_ship_position()
            return

        if dx != 0 or dy != 0:
            moved = self.player.move_system_map(dx, dy)
            if moved:
                self.fuel -= 1
                self.check_planet_visit()

    def check_planet_visit(self):
        px, py = self.player.board_x, self.player.board_y
        for planet in self.planets:
            if (px, py) == planet["pos"]:
                if not planet["visited"]:
                    planet["visited"] = True
                    self.trigger_planet_event(planet["name"])
                    if planet.get("is_fuel_planet", False):
                        self.fuel += 5
                    self.maybe_trigger_event()
                break

    def trigger_planet_event(self, planet_name: str) -> None:
        if planet_name in self.story_texts:
            for line in self.story_texts[planet_name]:
                self.display_text_blocking(line)
        ctype = self.get_next_challenge_type()

        if ctype == "task" and len(self.tasks_data) > 0:
            t = self.tasks_data.pop(0)
            #   scene = TaskScene(self.screen, self.overlay_surface, self.overlay_background, self.stats,
            #                  t["description"], t["solution"], t["group"])
            #  scene.run_scene()
        elif ctype == "quiz" and len(self.quiz_data) > 0:
            q = self.quiz_data.pop(0)
            # scene = QuizScene(self.screen, self.overlay_surface, self.overlay_background, self.stats,
            #                  q["question"], q["options"], q["correct_idx"], q["group"])
            # scene.run_scene()

    def get_next_challenge_type(self) -> str | None:
        if not self.tasks_data and not self.quiz_data:
            return None
        if not self.tasks_data:
            return "quiz"
        if not self.quiz_data:
            return "task"
        if random.random() < 0.3:
            return "quiz"
        return "task"

    def maybe_trigger_event(self) -> None:
        prob = EVENT_PROBABILITY
        if random.random() < prob:
            card = random.choice(self.event_cards)
            txt = f"{card['name']}: {card.get('description', 'No desc')}"
            self.display_text_blocking(txt)
            self.apply_event_effect(card)


    # ***** Scenes Helpers *****

    def apply_event_effect(self, card: dict) -> None:
        self.hull += card.get("hull_change", 0)
        self.fuel += card.get("fuel_change", 0)
        if self.hull <= 0:
            self.game_state = "game_over"

    def display_text_blocking(self, text: str) -> None:
        waiting = True
        overlay_height = 200
        while waiting:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    self.is_running = False
                    waiting = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key in [pygame.K_RETURN, pygame.K_SPACE]:
                        waiting = False

            if self.overlay_surface and self.overlay_background:
                self.overlay_surface.blit(self.overlay_background, (0, 0))
                self.render_simple_overlay(text, "[ENTER/SPACE] to continue", overlay_height)

    def render_simple_overlay(self, main_text: str, help_text: str, overlay_height: int) -> None:
        if not self.overlay_surface:
            return
        surf = pygame.Surface((self.overlay_surface.get_width(), overlay_height))
        surf.set_alpha(120)
        surf.fill(BLACK)
        by = self.overlay_surface.get_height() - overlay_height
        self.overlay_surface.blit(surf, (0, by))

        txt0 = pygame.font.Font().render(main_text, True, (255, 255, 255))
        txt1 = pygame.font.Font().render(help_text, True, (255, 255, 255))
        self.overlay_surface.blit(txt0, (20, by + 20))
        self.overlay_surface.blit(txt1, (20, by + 60))
        pygame.display.flip()
