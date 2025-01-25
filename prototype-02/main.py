#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
import random
import warnings
import pygame
from enum import Enum
from abc import ABC, abstractmethod
import os

# Nur noch:
from moviepy import VideoFileClip
from pygame import Surface

###############################################################################
# 1) LIBPNG-WARNUNGEN IGNORIEREN (OPTIONAL)
###############################################################################
warnings.filterwarnings("ignore", message="libpng warning")

###############################################################################
# 2) ENUM FÜR FARBEN
###############################################################################
class Color(Enum):
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DEBUG_BG = (40, 40, 60)
    GAME_BG = (20, 20, 40)
    PLAYER = (255, 60, 60)
    BUTTON_BG = (80, 80, 200)
    BUTTON_HOVER = (100, 100, 220)

###############################################################################
# VIDEO PLAYER FÜR INTRO
###############################################################################
class VideoPlayer:
    """
    Spielt ein Video (MP4) ab, inkl. Ton, mit moviepy.
    Stoppt bei Tastendruck oder Fenster-Schließen.
    """
    def __init__(self, screen: Surface):
        self.screen = screen
        self.video_path = None
        self.temp_folder = "temp"
        self.temp_audio_path = os.path.join(self.temp_folder, "temp_audio.mp3")

        if not os.path.exists(self.temp_folder):
            os.makedirs(self.temp_folder, exist_ok=True)

    def set_video(self, video_path: str):
        self.video_path = video_path

    def __render(self, clip: VideoFileClip):
        frame_duration = 1 / clip.fps
        last_frame_time = pygame.time.get_ticks()

        pygame.mixer.music.play()

        for frame in clip.iter_frames(fps=clip.fps, dtype="uint8", with_times=False):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    clip.close()
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    clip.close()
                    pygame.mixer.music.stop()
                    return

            frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
            frame_surface = pygame.transform.scale(frame_surface, self.screen.get_size())
            self.screen.blit(frame_surface, (0, 0))
            pygame.display.update()

            while (pygame.time.get_ticks() - last_frame_time) < frame_duration * 1000:
                pass
            last_frame_time = pygame.time.get_ticks()

    def play(self):
        if not self.video_path:
            print("Kein Video angegeben!")
            return

        clip = VideoFileClip(self.video_path)

        # Audio extrahieren
        clip.audio.write_audiofile(self.temp_audio_path, fps=44100)
        pygame.mixer.init()
        pygame.mixer.music.load(self.temp_audio_path)

        self.__render(clip)

        clip.close()
        pygame.mixer.music.stop()

###############################################################################
# 3) ABSTRAKTE KLASSE "GAME"
###############################################################################
class Game(ABC):
    def __init__(self):
        self.is_running = True

    @abstractmethod
    def handle_events(self):
        pass

    @abstractmethod
    def update(self, dt: float):
        pass

    @abstractmethod
    def draw(self):
        pass

    def stop(self):
        self.is_running = False

###############################################################################
# DEBUG MANAGER
###############################################################################
class DebugManager:
    def __init__(self):
        self.debug_mode = False
        self.hex_rows = 12
        self.hex_cols = 12
        self.hex_radius = 25
        self.offset_x = 65
        self.offset_y = 150

        # Sonnensystem-Bild
        self.bg_sonnen = None
        self.load_sonnensystem_image()

    def load_sonnensystem_image(self):
        try:
            self.bg_sonnen = pygame.image.load("../assets/Sonnensystem38x38.png").convert()
        except:
            self.bg_sonnen = pygame.Surface((500, 500))
            self.bg_sonnen.fill((0, 0, 0))

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode
        print(f"[DEBUG] Modus: {self.debug_mode}")

    def draw_debug(self, surface: pygame.Surface, game: "StoryGame"):
        if not self.debug_mode:
            surface.fill(Color.DEBUG_BG.value)
            return

        surface.fill(Color.BLACK.value)
        self.draw_sonnensystem_bg(surface)
        self.draw_hex_grid(surface)
        self.draw_planets_and_player(surface, game)
        self.draw_debug_info(surface, game)

    def draw_sonnensystem_bg(self, surface: pygame.Surface):
        surf_w, surf_h = surface.get_size()
        img_w, img_h = self.bg_sonnen.get_size()
        ratio_surf = surf_w / surf_h
        ratio_img = img_w / img_h

        if ratio_img > ratio_surf:
            new_w = surf_w
            new_h = int(new_w / ratio_img)
        else:
            new_h = surf_h
            new_w = int(new_h * ratio_img)

        scaled = pygame.transform.smoothscale(self.bg_sonnen, (new_w, new_h))
        x_pos = (surf_w - new_w) // 2
        y_pos = (surf_h - new_h) // 2
        surface.blit(scaled, (x_pos, y_pos))

    def draw_hex_grid(self, surface: pygame.Surface):
        for r in range(self.hex_rows):
            for c in range(self.hex_cols):
                cx, cy = self.get_hex_center(r, c)
                points = []
                for i in range(6):
                    angle = math.radians(60 * i - 30)
                    px = cx + self.hex_radius * math.cos(angle)
                    py = cy + self.hex_radius * math.sin(angle)
                    points.append((px, py))
                pygame.draw.polygon(surface, Color.WHITE.value, points, 2)

    def draw_planets_and_player(self, surface: pygame.Surface, game: "StoryGame"):
        for planet in game.planets:
            cx, cy = self.get_hex_center(planet.row, planet.col)
            pygame.draw.circle(surface, (0, 255, 0), (int(cx), int(cy)), 15)
            if planet.is_fuel_planet:
                pygame.draw.circle(surface, (255, 200, 50), (int(cx), int(cy)), 10)

        px, py = self.get_hex_center(game.player_row, game.player_col)
        pygame.draw.circle(surface, Color.PLAYER.value, (int(px), int(py)), 12)

    def draw_debug_info(self, surface: pygame.Surface, game: "StoryGame"):
        font = pygame.font.SysFont(None, 24)
        info_lines = [
            f"Debug Mode [D]",
            f"Fuel: {game.fuel}",
            f"Hull: {game.hull}",
            f"Pos(r={game.player_row}, c={game.player_col})",
            f"Current Planet: {game.current_planet.name if game.current_planet else 'None'}"
        ]
        y_off = 10
        for line in info_lines:
            surf = font.render(line, True, Color.WHITE.value)
            surface.blit(surf, (10, y_off))
            y_off += 25

    def get_hex_center(self, row: int, col: int):
        vertical_spacing = self.hex_radius * 1.5
        horizontal_spacing = math.sqrt(3) * self.hex_radius
        center_x = self.offset_x + col * horizontal_spacing + (row % 2) * (horizontal_spacing / 2)
        center_y = self.offset_y + row * vertical_spacing
        return center_x, center_y

###############################################################################
# 4) MODEL-KLASSEN: PLANET, STORY, EVENTCARD
###############################################################################
class Planet:
    def __init__(self, name, row, col, visited=False, is_fuel_planet=False, bg_image=None):
        self.name = name
        self.row = row
        self.col = col
        self.visited = visited
        self.is_fuel_planet = is_fuel_planet
        self.bg_image = bg_image

class Story:
    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.lines = lines

###############################################################################
# EVENT MANAGER
###############################################################################
class EventCard:
    """
    type => "positive" oder "negative"
    hull_change, fuel_change => Basiseffekte
    """
    def __init__(self, name, description, hull_change=0, fuel_change=0,
                 image=None, event_type="negative"):
        self.name = name
        self.description = description
        self.hull_change = hull_change
        self.fuel_change = fuel_change
        self.image = image
        self.type = event_type

class EventManager:
    def __init__(self, event_cards, base_probability=0.3):
        self.negative_events = [c for c in event_cards if c.type == "negative"]
        self.positive_events = [c for c in event_cards if c.type == "positive"]
        self.error_count = 0
        self.max_error = 5
        self.event_probability = base_probability

    def increase_error_count(self):
        if self.error_count < self.max_error:
            self.error_count += 1

    def decrease_error_count(self):
        if self.error_count > 0:
            self.error_count -= 1

    def should_trigger_event(self):
        return (random.random() < self.event_probability)

    def pick_event(self):
        # z.B. abhaengig von error_count
        neg_chance = 0.3 + (0.6 * (self.error_count / self.max_error))  # [0.3..0.9]
        if random.random() < neg_chance and self.negative_events:
            return random.choice(self.negative_events)
        else:
            if self.positive_events:
                return random.choice(self.positive_events)
            return None

    def apply_event_scaling(self, card: EventCard):
        if card.type == "negative":
            scale = 1.0 + (self.error_count * 0.5)
            if card.hull_change < 0:
                card.hull_change = int(card.hull_change * scale)
            if card.fuel_change < 0:
                card.fuel_change = int(card.fuel_change * scale)

###############################################################################
# STAR ENGINE
###############################################################################
class StarEngine:
    def __init__(self, width=1280, height=720, fps=60, title="Stardreck - DebugToggle"):
        pygame.init()
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.title_font = pygame.font.SysFont(None, 64)
        self.menu_font = pygame.font.SysFont(None, 36)

    def show_main_menu(self):
        button_width = 250
        button_height = 60
        button_x = (self.width - button_width) // 2
        button_y = (self.height - button_height) // 2

        while True:
            dt = self.clock.tick(self.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                    return "quit"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mx, my = event.pos
                        if (button_x <= mx <= button_x + button_width and
                            button_y <= my <= button_y + button_height):
                            return "storygame"

            self.screen.fill(Color.GAME_BG.value)

            title_surf = self.title_font.render("Stardreck", True, Color.WHITE.value)
            title_rect = title_surf.get_rect(center=(self.width // 2, 100))
            self.screen.blit(title_surf, title_rect)

            mx, my = pygame.mouse.get_pos()
            if (button_x <= mx <= button_x + button_width and
                button_y <= my <= button_y + button_height):
                pygame.draw.rect(self.screen, Color.BUTTON_HOVER.value,
                                 (button_x, button_y, button_width, button_height))
            else:
                pygame.draw.rect(self.screen, Color.BUTTON_BG.value,
                                 (button_x, button_y, button_width, button_height))

            text_surf = self.menu_font.render("Reise beginnen", True, Color.WHITE.value)
            text_rect = text_surf.get_rect(center=(button_x + button_width // 2,
                                                   button_y + button_height // 2))
            self.screen.blit(text_surf, text_rect)

            pygame.display.flip()

    def run(self, game: Game):
        while self.is_running and game.is_running:
            dt = self.clock.tick(self.fps) / 1000.0
            game.handle_events()
            game.update(dt)
            game.draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit()

###############################################################################
# 5) DATENKAPSELUNG: GAMEDATA
###############################################################################
class GameData:
    def __init__(self):
        planet_dicts = [
            {
                "name": "TerraNova",
                "row": 2,
                "col": 3,
                "visited": False,
                "bg_image": "../assets/welcome_screen.png"
            },
            {
                "name": "Mars",
                "row": 4,
                "col": 6,
                "visited": False,
                "isFuelPlanet": True,
                "bg_image": "../assets/welcome_screen.png"
            },
        ]
        self.planets = []
        for pd in planet_dicts:
            p = Planet(
                name=pd.get("name"),
                row=pd.get("row"),
                col=pd.get("col"),
                visited=pd.get("visited", False),
                is_fuel_planet=pd.get("isFuelPlanet", False),
                bg_image=pd.get("bg_image")
            )
            self.planets.append(p)

        self.story_segments = {
            "TerraNova": Story(lines=[
                "Willkommen auf Terra Nova! Hier begann eure Reise.",
                "Erkundet das System und findet wichtige Ressourcen.",
            ]),
            "Mars": Story(lines=[
                "Der Mars: Sandstürme und versteckte Alien-Signale!",
                "Vielleicht findet ihr Treibstoff in verlassenen Tanks.",
            ])
        }

        # Hier definieren wir positive / negative Events
        event_dicts = [
            {
                "name": "Asteroiden-Feld",
                "description": "Jemand hat die Toilette verstopft. Hull -1, Fuel -2",
                "hull_change": -1,
                "fuel_change": -2,
                "image": "../assets/welcome_screen.png",
                "type": "negative"
            },
            {
                "name": "Alter Satellit",
                "description": "Treibt im All. Fuel +2",
                "hull_change": 0,
                "fuel_change": 2,
                "image": "../assets/welcome_screen.png",
                "type": "positive"
            },
        ]
        self.event_cards = []
        for ed in event_dicts:
            ec = EventCard(
                name=ed["name"],
                description=ed["description"],
                hull_change=ed.get("hull_change", 0),
                fuel_change=ed.get("fuel_change", 0),
                image=ed.get("image"),
                event_type=ed.get("type", "negative")
            )
            self.event_cards.append(ec)

        self.event_probability = 1  # Grundsätzliche Event-Chance

        # Planetenspezifische Quiz
        self.planet_quizzes = {
            "TerraNova": [
                {
                    "type": "quiz",
                    "question": "TerraNova-spezifische Frage 1?",
                    "options": ["A", "B", "C", "D"],
                    "correct_idx": 0
                },
                {
                    "type": "task",
                    "question": "Wie groß ist G auf TerraNova? (m/s^2)",
                    "correct_value": 9.81
                }
            ],
            "Mars": [
                {
                    "type": "quiz",
                    "question": "Mars-spezifische Frage 1?",
                    "options": ["Eis", "Sand", "Lava", "Gras"],
                    "correct_idx": 1
                },
                {
                    "type": "task",
                    "question": "Mars Gravitation? (m/s^2)",
                    "correct_value": 3.711
                }
            ],
            "default": [
                {
                    "type": "quiz",
                    "question": "Leeres Feld: Frage 1?",
                    "options": ["Antwort1", "Antwort2", "Antwort3", "Antwort4"],
                    "correct_idx": 1
                },
                {
                    "type": "task",
                    "question": "Wie groß ist die Fluchtgeschwindigkeit? (m/s)",
                    "correct_value": 11186
                }
            ]
        }


###############################################################################
# STORY GAME
###############################################################################
class StoryGame(Game):
    def __init__(self, engine: StarEngine, data):
        super().__init__()
        self.engine = engine
        self.screen = engine.screen
        self.debug_manager = DebugManager()

        # Erzeuge den EventManager
        from_event_cards = data.event_cards
        self.event_manager = EventManager(from_event_cards, data.event_probability)

        self.planets = data.planets
        self.story_segments = data.story_segments

        # Original-Fragen
        self.planet_quizzes_init = data.planet_quizzes
        self.planet_quizzes_current = {}
        for pname, q_list in self.planet_quizzes_init.items():
            self.planet_quizzes_current[pname] = list(q_list)

        # Fuel = 50
        self.fuel = 50
        self.hull = 5

        self.player_row = 2
        self.player_col = 3
        self.current_planet = None

        self.debug_rect = pygame.Rect(0, 0, engine.width // 2, engine.height)
        self.game_rect = pygame.Rect(engine.width // 2, 0, engine.width // 2, engine.height)

        self.default_bg_full = None
        self.default_bg_half = None
        self.planet_bg_full = {}
        self.planet_bg_half = {}
        self.event_card_surfaces = {}

        self.load_backgrounds()
        self.load_event_assets()

    def load_backgrounds(self):
        try:
            img = pygame.image.load("../assets/welcome_screen.png").convert()
        except:
            img = pygame.Surface((self.engine.width, self.engine.height))
            img.fill(Color.GAME_BG.value)

        self.default_bg_full = pygame.transform.scale(img, (self.engine.width, self.engine.height))
        half_w = self.engine.width // 2
        half_h = self.engine.height
        self.default_bg_half = pygame.transform.scale(img, (half_w, half_h))

        for planet in self.planets:
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

    def load_event_assets(self):
        """Lade das generische Event-Karten-Bild,
           du kannst pro card.name evtl. eigenes Bild.
           Hier aber 'event_card.png' universal."""
        for card in self.event_manager.negative_events + self.event_manager.positive_events:
            # wir ignorieren card.image => override => "../assets/event_card.png"
            # damit alle dieselbe Karte haben
            universal_path = "../assets/event_card.png"
            try:
                surf = pygame.image.load(universal_path).convert_alpha()
            except:
                surf = pygame.Surface((200, 300))
                surf.fill((150, 0, 150))
            self.event_card_surfaces[card.name] = surf

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                elif event.key == pygame.K_d:
                    self.debug_manager.toggle_debug_mode()
                else:
                    self.handle_movement(event)

    def update(self, dt: float):
        pass

    def draw(self):
        planet_name = self.current_planet.name if self.current_planet else None

        if self.debug_manager.debug_mode:
            debug_surface = self.screen.subsurface(self.debug_rect)
            self.debug_manager.draw_debug(debug_surface, self)

            game_surface = self.screen.subsurface(self.game_rect)
            if planet_name and planet_name in self.planet_bg_half:
                game_surface.blit(self.planet_bg_half[planet_name], (0, 0))
            else:
                game_surface.blit(self.default_bg_half, (0, 0))
            self.draw_hud(game_surface)
        else:
            if planet_name and planet_name in self.planet_bg_full:
                self.screen.blit(self.planet_bg_full[planet_name], (0, 0))
            else:
                self.screen.blit(self.default_bg_full, (0, 0))
            self.draw_hud(self.screen)

    def handle_movement(self, event):
        dr, dc = 0, 0
        if event.key == pygame.K_UP:
            dr = -1
        elif event.key == pygame.K_DOWN:
            dr = 1
        elif event.key == pygame.K_LEFT:
            dc = -1
        elif event.key == pygame.K_RIGHT:
            dc = 1

        if (dr != 0 or dc != 0) and self.fuel > 0:
            self.player_row += dr
            self.player_col += dc
            self.fuel -= 1
            self.check_planet_visit()
        elif (dr != 0 or dc != 0):
            self.game_over("Kein Treibstoff mehr!")

    def check_planet_visit(self):
        self.current_planet = None
        found_planet = False

        for planet in self.planets:
            if planet.row == self.player_row and planet.col == self.player_col:
                self.current_planet = planet
                found_planet = True
                if not planet.visited:
                    planet.visited = True
                    self.trigger_planet_event(planet)
                break

        # => Event ? (auch auf leerem Feld)
        if self.event_manager.should_trigger_event():
            self.trigger_random_event()

        if not found_planet:
            quiz_data = self.get_random_quiz_for_planet("default")
            if quiz_data:
                self.run_quiz_scene(quiz_data)

    def trigger_planet_event(self, planet):
        if planet.name in self.story_segments:
            for line in self.story_segments[planet.name].lines:
                self.display_text_blocking(line)

        # Planetenspezifisches Quiz
        quiz_data = self.get_random_quiz_for_planet(planet.name)
        if quiz_data:
            self.run_quiz_scene(quiz_data)

        if planet.is_fuel_planet:
            self.fuel += 5
            self.display_text_blocking("Ihr habt +5 Fuel gefunden!")

    def trigger_random_event(self):
        card = self.event_manager.pick_event()
        if not card:
            return
        self.event_manager.apply_event_scaling(card)
        # => Animiertes Darstellen
        self.display_event_card_animated(card)

        self.fuel += card.fuel_change
        self.hull += card.hull_change
        if self.hull <= 0:
            self.game_over("Hull <= 0. Zerstört!")

    ###########################################################################
    # QUIZ
    ###########################################################################
    def get_random_quiz_for_planet(self, planet_name):
        if planet_name not in self.planet_quizzes_current:
            return None
        qlist = self.planet_quizzes_current[planet_name]
        if not qlist:
            # Neu laden
            self.planet_quizzes_current[planet_name] = list(self.planet_quizzes_init[planet_name])
            qlist = self.planet_quizzes_current[planet_name]
        if not qlist:
            return None

        idx = random.randrange(len(qlist))
        return qlist.pop(idx)

    def run_quiz_scene(self, quiz_data):
        q_type = quiz_data.get("type", "quiz")
        if q_type == "quiz":
            self.run_quiz_multiple_choice(quiz_data)
        else:
            self.run_quiz_task(quiz_data)

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
                                self.display_text_blocking("Richtig beantwortet!")
                                self.event_manager.decrease_error_count()
                            else:
                                self.display_text_blocking("Falsch! Hull -1.")
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
            lines.append(f"Antwort eingeben (0-{len(options)-1}): {typed_input}")

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
                                self.display_text_blocking("Richtig beantwortet!")
                                self.event_manager.decrease_error_count()
                            else:
                                self.display_text_blocking("Falsch! Hull -1.")
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
    # ANIMATION EVENT-KARTE
    ###########################################################################
    def display_event_card_animated(self, card):
        """
        Animiert die event_card.png:
         1) fliegt von unten nach oben in 1s
         2) rotiert um 360 Grad in demselben Zeitraum
         3) Unterhalb der Karte der event-Text
         4) Klick => schließt
        """
        waiting = True
        # 1) Delta time
        clock = pygame.time.Clock()
        startTime = pygame.time.get_ticks()
        duration = 1000  # ms (1 Sek)

        # Lade die Event-Karte
        cardSurf = self.event_card_surfaces.get(card.name, None)
        if not cardSurf:
            # fallback
            w, h = 200, 300
            cardSurf = pygame.Surface((w, h))
            cardSurf.fill((150, 0, 150))

        # Seitenverhältnis => 509x892 => hier z.B. 200px breit => 200 / 509 => height ~ 351
        # Du kannst beliebig skalieren
        # Hier skalieren wir, so dass Breite= 200 => Höhe= about 351
        target_w = 200
        ratio = cardSurf.get_width() / cardSurf.get_height()
        target_h = int(target_w / ratio)
        cardSurf = pygame.transform.smoothscale(cardSurf, (target_w, target_h))

        # 2) Animationsschleife
        #   yStart = +200px unter dem center => centerY + 200
        #   yEnd   = centerY
        #   angleStart=0, angleEnd=360
        #   text unterhalb
        target_surf = (self.screen.subsurface(self.game_rect)
                       if self.debug_manager.debug_mode
                       else self.screen)
        sw = target_surf.get_width()
        sh = target_surf.get_height()
        centerX = sw // 2
        centerY = sh // 2

        textFont = pygame.font.SysFont(None, 24)
        textLines = self.wrap_text(card.description, textFont, sw - 20)

        # Animationsvariablen
        animRunning = True
        angle = 0.0
        while waiting and self.is_running:
            dt = clock.tick(60)
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Klick => beende
                    waiting = False
                    break

            self.draw()  # Hintergrund

            # Target surface
            if self.debug_manager.debug_mode:
                target_surf = self.screen.subsurface(self.game_rect)
            else:
                target_surf = self.screen
            sw = target_surf.get_width()
            sh = target_surf.get_height()

            elapsed = pygame.time.get_ticks() - startTime
            frac = elapsed / duration
            if frac >= 1.0:
                frac = 1.0
                animRunning = False

            # Position => y = centerY + 200*(1-frac)
            currentY = centerY + 200*(1-frac)
            # Rotation => angle = 360 * frac
            angle = 360.0 * frac

            # Rotiertes Bild
            rotSurf = pygame.transform.rotate(cardSurf, angle)
            rw, rh = rotSurf.get_width(), rotSurf.get_height()
            # zentrieren
            xPos = (sw - rw)//2
            yPos = int(currentY - rh//2)

            # Blit
            target_surf.blit(rotSurf, (xPos, yPos))

            # Danach Text darunter
            # offset ~ 10 px
            textOverlay = pygame.Surface((sw, 100))
            textOverlay.set_alpha(180)
            textOverlay.fill(Color.BLACK.value)
            # z.B. y= yPos + rh + 10
            textRect = pygame.Rect(0, yPos + rh + 10, sw, 100)

            y_off = 10
            for line in textLines:
                lineImg = textFont.render(line, True, Color.WHITE.value)
                textOverlay.blit(lineImg, (10, y_off))
                y_off += lineImg.get_height() + 5

            target_surf.blit(textOverlay, (textRect.x, textRect.y))

            pygame.display.flip()

            # Falls anim schon fertig und user nicht geklickt => bleibe => break
            if not animRunning:
                # Nach der Animation => user klick => close
                pass

        # Ende => wir kehren zurück

    def draw_hud(self, surface: pygame.Surface):
        font = pygame.font.SysFont(None, 28)
        hud_line = f"Fuel: {self.fuel} | Hull: {self.hull}"
        surf = font.render(hud_line, True, Color.WHITE.value)
        surface.blit(surf, (20, 20))

    def display_text_blocking(self, text: str):
        waiting = True
        font = pygame.font.SysFont(None, 24)

        if self.debug_manager.debug_mode:
            target_surf = self.screen.subsurface(self.game_rect)
            ow_w = self.game_rect.width
            ow_h = 180
        else:
            target_surf = self.screen
            ow_w = self.screen.get_width()
            ow_h = 180

        overlay_rect = pygame.Rect(0, target_surf.get_height() - ow_h, ow_w, ow_h)

        clock = pygame.time.Clock()
        while waiting and self.is_running:
            dt = clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                        waiting = False
                    elif event.key == pygame.K_d:
                        self.debug_manager.toggle_debug_mode()
                    elif event.key == pygame.K_ESCAPE:
                        self.stop()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False

            self.draw()

            text_overlay = pygame.Surface((ow_w, ow_h))
            text_overlay.set_alpha(180)
            text_overlay.fill(Color.BLACK.value)

            lines = self.wrap_text(text, font, ow_w - 20)
            y_off = 10
            for line in lines:
                line_img = font.render(line, True, Color.WHITE.value)
                text_overlay.blit(line_img, (10, y_off))
                y_off += line_img.get_height() + 5

            target_surf.blit(text_overlay, (overlay_rect.x, overlay_rect.y))
            pygame.display.flip()

    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int):
        words = text.split(" ")
        lines = []
        current_line = ""
        for w in words:
            test_line = current_line + w + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = w + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    def game_over(self, reason: str):
        print("GAME OVER:", reason)
        self.display_text_blocking(f"GAME OVER: {reason}")
        self.stop()

###############################################################################
# MAIN
###############################################################################
def main():
    # Intro-Video
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Stardreck IntroVideo")

    player = VideoPlayer(screen)
    player.set_video("../assets/test_video01.mp4")
    player.play()

    # Starte Engine
    engine = StarEngine(1280, 720, 60, "Stardreck - DebugToggle")

    # Hauptmenü
    menu_result = engine.show_main_menu()
    if menu_result == "quit":
        return

    if menu_result == "storygame":
        from_data = GameData()
        game = StoryGame(engine, from_data)
        engine.run(game)

if __name__ == "__main__":
    main()
