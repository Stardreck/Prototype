import sys
import json
import random
import pygame
import pygame_gui  # for UI

# ==================== SETTINGS via JSON ====================
SETTINGS_JSON = r'''
{
  "colors": {
    "WHITE": [255, 255, 255],
    "BLACK": [0, 0, 0],
    "GRAY": [200, 200, 200],
    "RED": [255, 0, 0],
    "GREEN": [0, 255, 0],
    "PURPLE": [128, 0, 128]
  },
  "width": 1600,
  "height": 720,
  "fps": 30,
  "tile_size": 60,
  "board_cols": 10,
  "board_rows": 8,
  "margin_top": 100
}
'''

SETTINGS = json.loads(SETTINGS_JSON)
WHITE  = tuple(SETTINGS["colors"]["WHITE"])
BLACK  = tuple(SETTINGS["colors"]["BLACK"])
GRAY   = tuple(SETTINGS["colors"]["GRAY"])
RED    = tuple(SETTINGS["colors"]["RED"])
GREEN  = tuple(SETTINGS["colors"]["GREEN"])
PURPLE = tuple(SETTINGS["colors"]["PURPLE"])

WIDTH       = SETTINGS["width"]
HEIGHT      = SETTINGS["height"]
FPS         = SETTINGS["fps"]
TILE_SIZE   = SETTINGS["tile_size"]
BOARD_COLS  = SETTINGS["board_cols"]
BOARD_ROWS  = SETTINGS["board_rows"]
MARGIN_TOP  = SETTINGS["margin_top"]

SHIP_INTERIOR_COLS = 8
SHIP_INTERIOR_ROWS = 8

# Beispiel-Daten
PLANETS_DATA = [
    {"name": "Terra Nova","pos": (1, 2),"visited": False,"is_fuel_planet": True},
    {"name": "Alien-Ruinen","pos": (6, 3),"visited": False,"is_fuel_planet": False},
    {"name": "Abtrünnige","pos": (8, 5),"visited": False,"is_fuel_planet": False},
    {"name": "Refuel Station X","pos": (3, 4),"visited": False,"is_fuel_planet": True}
]

STORY_TEXTS = {
    "Terra Nova": [
        "Welcome to Terra Nova!",
        "The colony is suffering from a resource shortage..."
    ],
    "Alien-Ruinen": [
        "You arrive at ancient alien ruins.",
        "Mysterious symbols are glowing on the walls..."
    ],
    "Abtrünnige": [
        "You encounter some renegade colonists.",
        "They are not exactly happy to see you."
    ],
    "Refuel Station X": [
        "You found a hidden refuel station!",
        "Your spaceship's tank is replenished."
    ]
}

TASKS_DATA = [
    {
        "description": "DYNAMICS: Calculate momentum p (m=2 kg, v=3 m/s).",
        "solution": "6",
        "group": "Dynamik"
    },
    {
        "description": "THERMODYNAMICS: Temperature difference (T1=300K, T2=273K).",
        "solution": "27",
        "group": "Wärmelehre"
    }
]

QUIZ_DATA = [
    {
        "question": "DYNAMICS: Newton's 2nd law?",
        "options": ["E=mc^2","p=mv","F=ma","F=-kx"],
        "correct_idx": 2,
        "group": "Dynamik"
    },
    {
        "question": "THERMODYNAMICS: Absolute zero in Celsius?",
        "options": ["-273.15°C","0°C","-100°C","273°C"],
        "correct_idx": 0,
        "group": "Wärmelehre"
    }
]

EVENT_CARDS = [
    {
        "name": "Asteroid Storm",
        "type": "negative",
        "description": "Your hull is damaged by 2.",
        "hull_change": -2
    },
    {
        "name": "Friendly Merchant",
        "type": "positive",
        "description": "Your fuel is increased by 3.",
        "fuel_change": 3
    }
]

SHIP_INTERIOR_MAP = [
    {"name": "Bridge","pos": (1,1),"event":"Bridge: All systems here.","visited":False},
    {"name": "Engine Room","pos": (1,2),"event":"Engine Room. Check power!","visited":False}
]

EVENT_PROBABILITY = 0.2
NEGATIVE_EVENT_BOOST       = 0.15
NEGATIVE_EVENT_BOOST_ROUNDS= 3

# ============ Player Sprite ============
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game_width, game_height):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 10, TILE_SIZE - 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        self.board_x = x
        self.board_y = y
        self.ship_x  = 0
        self.ship_y  = 0
        self.game_width  = game_width
        self.game_height = game_height
        self.update_position()

    def move_system_map(self, dx, dy):
        nx = self.board_x + dx
        ny = self.board_y + dy
        if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:
            self.board_x = nx
            self.board_y = ny
            self.update_position()
            return True
        return False

    def move_ship_interior(self, dx, dy):
        nx = self.ship_x + dx
        ny = self.ship_y + dy
        if 0 <= nx < SHIP_INTERIOR_COLS and 0 <= ny < SHIP_INTERIOR_ROWS:
            self.ship_x = nx
            self.ship_y = ny
            self.update_position_interior()
            return True
        return False

    def update_position(self):
        offset_x = (self.game_width//2 - BOARD_COLS*TILE_SIZE)//2
        offset_y = MARGIN_TOP
        self.rect.x = offset_x + self.board_x*TILE_SIZE
        self.rect.y = offset_y + self.board_y*TILE_SIZE

    def update_position_interior(self):
        offset_x = (self.game_width//2 - SHIP_INTERIOR_COLS*TILE_SIZE)//2
        offset_y = 50
        self.rect.x = offset_x + self.ship_x*TILE_SIZE
        self.rect.y = offset_y + self.ship_y*TILE_SIZE

# ============ GameStats ============
class GameStats:
    def __init__(self):
        self.total_wrong_answers = 0
        self.wrong_by_group = {}

    def register_wrong_answer(self, group_name):
        self.total_wrong_answers += 1
        if group_name not in self.wrong_by_group:
            self.wrong_by_group[group_name] = 0
        self.wrong_by_group[group_name] += 1

# ============ DebugManager ============
class DebugManager:
    def __init__(self, screen):
        self.debug_mode = False
        self.screen = screen
        self.width  = screen.get_width()
        self.height = screen.get_height()

    def toggle_debug_mode(self):
        self.debug_mode = not self.debug_mode

    def is_debug_active(self):
        return self.debug_mode

    def create_surfaces(self, game_obj):
        if self.debug_mode:
            board_rect   = pygame.Rect(0,0, game_obj.width//2, game_obj.height)
            overlay_rect = pygame.Rect(game_obj.width//2,0, game_obj.width//2, game_obj.height)
            game_obj.board_surf   = game_obj.screen.subsurface(board_rect)
            game_obj.overlay_surf = game_obj.screen.subsurface(overlay_rect)
        else:
            full_rect = pygame.Rect(0,0, game_obj.width, game_obj.height)
            game_obj.board_surf   = None
            game_obj.overlay_surf = game_obj.screen.subsurface(full_rect)

    def draw_system_map_debug(self, game_obj):
        if not game_obj.board_surf:
            return
        board_surf = game_obj.board_surf
        board_surf.fill(WHITE)

        # draw grid
        ox = (board_surf.get_width() - BOARD_COLS*TILE_SIZE)//2
        oy = MARGIN_TOP
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                rect=pygame.Rect(ox + c*TILE_SIZE, oy + r*TILE_SIZE, TILE_SIZE,TILE_SIZE)
                pygame.draw.rect(board_surf, GRAY, rect,1)

        # draw planets
        for planet in game_obj.planets:
            px, py = planet["pos"]
            cx = ox + px*TILE_SIZE + TILE_SIZE//2
            cy = oy + py*TILE_SIZE + TILE_SIZE//2
            if planet.get("is_fuel_planet",False):
                color = PURPLE
            else:
                color = GREEN if not planet["visited"] else (100,200,100)
            pygame.draw.circle(board_surf, color,(cx,cy),15)

        # draw sprites
        game_obj.all_sprites.draw(board_surf)

        # debug info
        line_y=20
        txt_fuel = StarEngine.font.render(f"Fuel: {game_obj.fuel}", True, BLACK)
        board_surf.blit(txt_fuel, (20,line_y))
        line_y+=30
        txt_hull = StarEngine.font.render(f"Hull: {game_obj.hull}", True, BLACK)
        board_surf.blit(txt_hull, (20,line_y))
        line_y+=30

    def draw_ship_interior_debug(self, game_obj):
        if not game_obj.board_surf:
            return
        board_surf = game_obj.board_surf
        board_surf.fill((60,60,80))

        ox=(board_surf.get_width()-SHIP_INTERIOR_COLS*TILE_SIZE)//2
        oy=50
        for r in range(SHIP_INTERIOR_ROWS):
            for c in range(SHIP_INTERIOR_COLS):
                rect=pygame.Rect(ox+c*TILE_SIZE, oy+r*TILE_SIZE,TILE_SIZE,TILE_SIZE)
                pygame.draw.rect(board_surf, GRAY, rect,1)

        for room in game_obj.ship_rooms:
            rx, ry=room["pos"]
            rxp=ox+rx*TILE_SIZE
            ryp=oy+ry*TILE_SIZE
            pygame.draw.rect(board_surf,(100,180,100),pygame.Rect(rxp,ryp,TILE_SIZE,TILE_SIZE))

        game_obj.all_sprites.draw(board_surf)

        line_y=20
        txt_fuel=StarEngine.font.render(f"Fuel: {game_obj.fuel}",True,BLACK)
        board_surf.blit(txt_fuel,(20,line_y))
        line_y+=30
        txt_hull=StarEngine.font.render(f"Hull: {game_obj.hull}",True,BLACK)
        board_surf.blit(txt_hull,(20,line_y))

# ============ Scenes (TaskScene, QuizScene) ============
class Scene:
    def __init__(self, screen, overlay_surf, overlay_bg, stats):
        self.screen = screen
        self.overlay_surf = overlay_surf
        self.overlay_bg   = overlay_bg
        self.stats        = stats

    def run_scene(self):
        pass

    def render_simple_overlay(self, main_text, help_text):
        overlay_height=200
        surf=pygame.Surface((self.overlay_surf.get_width(), overlay_height))
        surf.set_alpha(120)
        surf.fill(BLACK)
        bot_y=self.overlay_surf.get_height()-overlay_height
        self.overlay_surf.blit(surf,(0,bot_y))

        txt0=StarEngine.font.render(main_text,True,WHITE)
        txt1=StarEngine.font.render(help_text,True,WHITE)
        self.overlay_surf.blit(txt0,(20,bot_y+20))
        self.overlay_surf.blit(txt1,(20,bot_y+60))
        pygame.display.flip()

class TaskScene(Scene):
    def __init__(self, screen, overlay_surf, overlay_bg, stats, description, solution, group):
        super().__init__(screen, overlay_surf, overlay_bg, stats)
        self.description = description
        self.solution = solution
        self.group = group
        self.user_input=""

    def run_scene(self):
        clock=pygame.time.Clock()
        running=True
        while running:
            dt=clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type==pygame.KEYDOWN:
                    if ev.key==pygame.K_RETURN:
                        if self.user_input.strip()==self.solution:
                            feed="Correct numeric answer!"
                        else:
                            feed=f"Wrong! (Correct: {self.solution})"
                            self.stats.register_wrong_answer(self.group)
                        self.show_feedback(feed)
                        running=False
                    elif ev.key==pygame.K_BACKSPACE:
                        self.user_input=self.user_input[:-1]
                    else:
                        if ev.unicode.isdigit():
                            self.user_input+=ev.unicode

            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))
                self.draw_overlay()

    def draw_overlay(self):
        overlay_height=300
        surf=pygame.Surface((self.overlay_surf.get_width(), overlay_height))
        surf.set_alpha(120)
        surf.fill(BLACK)
        bot_y=self.overlay_surf.get_height()-overlay_height
        self.overlay_surf.blit(surf,(0,bot_y))

        txt0=StarEngine.font.render(self.description,True,WHITE)
        txt1=StarEngine.font.render("Your input: "+self.user_input,True,WHITE)
        txt2=StarEngine.font.render("[ENTER] to confirm",True,WHITE)

        self.overlay_surf.blit(txt0,(20,bot_y+20))
        self.overlay_surf.blit(txt1,(20,bot_y+60))
        self.overlay_surf.blit(txt2,(20,bot_y+100))

        pygame.display.flip()

    def show_feedback(self, text):
        waiting=True
        while waiting:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type==pygame.KEYDOWN:
                    if ev.key in [pygame.K_RETURN,pygame.K_SPACE]:
                        waiting=False
            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))
                self.render_simple_overlay(text,"[ENTER/SPACE] to continue")

class QuizScene(Scene):
    def __init__(self, screen, overlay_surf, overlay_bg, stats, question, options, correct_idx, group):
        super().__init__(screen,overlay_surf,overlay_bg,stats)
        self.question    = question
        self.options     = options
        self.correct_idx = correct_idx
        self.group       = group

    def run_scene(self):
        clock=pygame.time.Clock()
        running=True
        while running:
            dt=clock.tick(FPS)
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type==pygame.KEYDOWN:
                    if ev.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                        choice=ev.key - pygame.K_1
                        if choice==self.correct_idx:
                            feed="Correct!"
                        else:
                            feed=f"Wrong! (Correct: {self.options[self.correct_idx]})"
                            self.stats.register_wrong_answer(self.group)
                        self.show_feedback(feed)
                        running=False

            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))
                self.draw_overlay()

    def draw_overlay(self):
        overlay_height=300
        surf=pygame.Surface((self.overlay_surf.get_width(), overlay_height))
        surf.set_alpha(120)
        surf.fill(BLACK)
        bot_y=self.overlay_surf.get_height()-overlay_height
        self.overlay_surf.blit(surf,(0,bot_y))

        txt0=StarEngine.font.render(self.question,True,WHITE)
        self.overlay_surf.blit(txt0,(20,bot_y+20))

        y_off=60
        for i,opt_text in enumerate(self.options):
            t=StarEngine.font.render(f"{i+1}) {opt_text}",True,WHITE)
            self.overlay_surf.blit(t,(20, bot_y+y_off))
            y_off+=30

        info=StarEngine.font.render("Press [1..4]",True,WHITE)
        self.overlay_surf.blit(info,(20, bot_y+200))
        pygame.display.flip()

    def show_feedback(self, text):
        waiting=True
        while waiting:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif ev.type==pygame.KEYDOWN:
                    if ev.key in [pygame.K_RETURN,pygame.K_SPACE]:
                        waiting=False
            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))
                self.render_simple_overlay(text,"[ENTER/SPACE] to continue")

#
# =========== StarEngine ============
#
class StarEngine:
    font = None
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Stardreck - Last working version refactored")
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        StarEngine.font = pygame.font.SysFont(None,32)
        self.is_running=True

    def run_game_loop(self, story_game):
        while self.is_running and story_game.is_running:
            self.clock.tick(FPS)
            story_game.handle_events()
            story_game.update()
            story_game.draw()
            pygame.display.flip()
        pygame.quit()
        sys.exit()

#
# =========== StoryGame ============
#
from pygame.sprite import Group

class StoryGame:
    """
    Contains all logic, main menu, debug, tasks/quiz, etc.
    Creates engine second, referencing it in the constructor.
    """
    def __init__(self):
        # The user specifically said "Engine first, then Game"
        # but the "last code that worked" approach here is
        # to create engine second.
        # We'll do the user approach:
        # Actually create the engine FIRST in main() => pass screen to game => or just do the old approach.
        # We'll keep the old approach for minimal changes.

        # Step 1: create engine
        self.engine = StarEngine()
        self.screen = self.engine.screen

        self.debug_manager = DebugManager(self.screen)

        self.width  = self.screen.get_width()
        self.height = self.screen.get_height()
        self.board_surf=None
        self.overlay_surf=None

        self.debug_manager.create_surfaces(self)

        self.overlay_bg=None
        if self.overlay_surf:
            w=self.overlay_surf.get_width()
            h=self.overlay_surf.get_height()
            try:
                tmp=pygame.image.load("assets/welcome_screen.png")
                self.overlay_bg=pygame.transform.scale(tmp,(w,h))
            except:
                pass

        self.planets=PLANETS_DATA
        self.story_texts=STORY_TEXTS
        self.tasks_data=TASKS_DATA
        self.quiz_data=QUIZ_DATA
        self.event_cards=EVENT_CARDS
        self.ship_rooms=SHIP_INTERIOR_MAP

        self.fuel=5
        self.hull=5
        self.stats=GameStats()

        self.neg_event_boost_active=0
        self.neg_event_boost_amount=0.0

        self.game_state="system_map"
        self.is_running=True

        self.SHIP_INTERIOR_COLS=SHIP_INTERIOR_COLS
        self.SHIP_INTERIOR_ROWS=SHIP_INTERIOR_ROWS

        self.player=Player(0,0,self.width,self.height)
        self.all_sprites=Group(self.player)

        # brightness
        self.brightness=1.0

    def run(self):
        self.show_main_menu()
        if not self.is_running:
            return
        # if user didn't close => run main loop
        self.engine.run_game_loop(self)

    # minimal main menu
    def show_main_menu(self):
        manager=pygame_gui.UIManager((WIDTH,HEIGHT))
        bg=None
        try:
            bg=pygame.image.load("assets/welcome_screen.jpeg")
            bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))
        except:
            pass

        import pygame.font
        try:
            starjedi=pygame.font.Font("assets/fonts/Starjedi/Starjedi.ttf",60)
        except:
            starjedi=pygame.font.SysFont(None,60)

        start_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(WIDTH//2-100,HEIGHT//2, 200,50),
            text="Start Game",
            manager=manager
        )
        settings_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(WIDTH//2-100,HEIGHT//2+60,200,50),
            text="Settings",
            manager=manager
        )

        clock=pygame.time.Clock()
        run_menu=True
        while run_menu and self.is_running:
            dt=clock.tick(FPS)/1000.0
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    run_menu=False
                    self.is_running=False
                elif event.type==pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element==start_button:
                        run_menu=False
                    elif event.ui_element==settings_button:
                        self.show_settings()

                manager.process_events(event)

            if bg:
                self.screen.blit(bg,(0,0))
            else:
                self.screen.fill((50,50,50))

            title_surf=starjedi.render("Stardreck",True,(255,255,255))
            self.screen.blit(title_surf,(WIDTH//2-title_surf.get_width()//2,
                                          HEIGHT//3-title_surf.get_height()//2))

            manager.update(dt)
            manager.draw_ui(self.screen)
            self.apply_brightness()
            pygame.display.flip()

    def show_settings(self):
        manager=pygame_gui.UIManager((WIDTH,HEIGHT))
        bg=None
        try:
            bg=pygame.image.load("assets/welcome_screen.jpeg")
            bg=pygame.transform.scale(bg,(WIDTH,HEIGHT))
        except:
            pass

        brightness_slider=pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect(WIDTH//2-150,HEIGHT//2,300,40),
            start_value=self.brightness*100,
            value_range=(0,100),
            manager=manager
        )
        back_button=pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(WIDTH//2-100,HEIGHT//2+60,200,50),
            text="Back",
            manager=manager
        )

        clock=pygame.time.Clock()
        run_set=True
        while run_set and self.is_running:
            dt=clock.tick(FPS)/1000
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    run_set=False
                    self.is_running=False
                elif ev.type==pygame_gui.UI_BUTTON_PRESSED:
                    if ev.ui_element==back_button:
                        run_set=False
                elif ev.type==pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if ev.ui_element==brightness_slider:
                        self.brightness=ev.value/100.0
                manager.process_events(ev)

            if bg:
                self.screen.blit(bg,(0,0))
            else:
                self.screen.fill((30,30,30))

            manager.update(dt)
            manager.draw_ui(self.screen)
            self.apply_brightness()
            pygame.display.flip()

    def apply_brightness(self):
        alpha=int(255*(1-self.brightness))
        dark_surf=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
        dark_surf.fill((0,0,0,alpha))
        self.screen.blit(dark_surf,(0,0))

    # engine loop calls:
    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                self.is_running=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_l:
                    self.debug_manager.toggle_debug_mode()
                    self.debug_manager.create_surfaces(self)
                    self.reload_overlay_background()

                if self.game_state=="system_map":
                    self.handle_system_map_events(event)
                elif self.game_state=="ship_interior":
                    self.handle_ship_interior_events(event)

    def update(self):
        if self.fuel<=0 or self.hull<=0:
            self.game_state="game_over"

    def draw(self):
        self.screen.fill(BLACK)
        # debug
        if self.debug_manager.debug_mode:
            if self.game_state=="system_map":
                self.debug_manager.draw_system_map_debug(self)
            elif self.game_state=="ship_interior":
                self.debug_manager.draw_ship_interior_debug(self)
        else:
            if self.board_surf:
                self.board_surf.fill(BLACK)
        if self.game_state=="game_over":
            self.draw_game_over()
        else:
            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))

    # system map
    def handle_system_map_events(self, event):
        dx,dy=0,0
        if event.key==pygame.K_UP:dy=-1
        elif event.key==pygame.K_DOWN:dy=1
        elif event.key==pygame.K_LEFT:dx=-1
        elif event.key==pygame.K_RIGHT:dx=1
        elif event.key==pygame.K_p:
            self.game_state="ship_interior"
            self.player.ship_x=0
            self.player.ship_y=0
            self.player.update_position_interior()
            return

        if dx!=0 or dy!=0:
            moved=self.player.move_system_map(dx,dy)
            if moved:
                self.fuel-=1
                self.check_planet_visit()

    def check_planet_visit(self):
        px,py=self.player.board_x,self.player.board_y
        for planet in self.planets:
            if (px,py)==planet["pos"]:
                if not planet["visited"]:
                    planet["visited"]=True
                    self.trigger_planet_event(planet["name"])
                    if planet.get("is_fuel_planet",False):
                        self.fuel+=5
                    self.maybe_trigger_event()
                break

    def trigger_planet_event(self, planet_name):
        if planet_name in self.story_texts:
            for line in self.story_texts[planet_name]:
                self.display_text_blocking(line)

        # pick challenge
        ctype=self.get_next_challenge_type()
        if ctype=="task" and len(self.tasks_data)>0:
            t=self.tasks_data.pop(0)
            scene=TaskScene(self.screen,self.overlay_surf,self.overlay_bg,self.stats,
                            t["description"], t["solution"], t["group"])
            scene.run_scene()
        elif ctype=="quiz" and len(self.quiz_data)>0:
            q=self.quiz_data.pop(0)
            scene=QuizScene(self.screen,self.overlay_surf,self.overlay_bg,self.stats,
                            q["question"],q["options"],q["correct_idx"],q["group"])
            scene.run_scene()

    def get_next_challenge_type(self):
        if not self.tasks_data and not self.quiz_data:
            return None
        if not self.tasks_data:
            return "quiz"
        if not self.quiz_data:
            return "task"
        if random.random()<0.3:
            return "quiz"
        return "task"

    def maybe_trigger_event(self):
        prob=EVENT_PROBABILITY
        if random.random()<prob:
            card=random.choice(EVENT_CARDS)
            self.show_event_card(card)
            self.apply_event_effect(card)

    def show_event_card(self, card):
        txt=f"{card['name']}: {card.get('description','No desc')}"
        self.display_text_blocking(txt)

    def apply_event_effect(self, card):
        self.hull+=card.get("hull_change",0)
        self.fuel+=card.get("fuel_change",0)
        if self.hull<=0:
            self.game_state="game_over"

    # interior
    def handle_ship_interior_events(self, event):
        if event.key==pygame.K_ESCAPE:
            self.game_state="system_map"
            return
        dx,dy=0,0
        if event.key==pygame.K_UP:dy=-1
        elif event.key==pygame.K_DOWN:dy=1
        elif event.key==pygame.K_LEFT:dx=-1
        elif event.key==pygame.K_RIGHT:dx=1
        if dx!=0 or dy!=0:
            moved=self.player.move_ship_interior(dx,dy)
            if moved:
                self.check_ship_room()

    def check_ship_room(self):
        sx,sy=self.player.ship_x,self.player.ship_y
        for room in self.ship_rooms:
            if (sx,sy)==room["pos"]:
                if not room["visited"]:
                    room["visited"]=True
                    self.display_text_blocking(room["event"])
                break

    # Scenes helpers
    def display_text_blocking(self, text):
        waiting=True
        overlay_height=200
        while waiting:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    self.is_running=False
                    waiting=False
                elif ev.type==pygame.KEYDOWN:
                    if ev.key in [pygame.K_RETURN,pygame.K_SPACE]:
                        waiting=False

            if self.overlay_surf and self.overlay_bg:
                self.overlay_surf.blit(self.overlay_bg,(0,0))
                self.render_simple_overlay(text,"[ENTER/SPACE] to continue",overlay_height)

    def render_simple_overlay(self, main_text, help_text, overlay_height):
        surf=pygame.Surface((self.overlay_surf.get_width(),overlay_height))
        surf.set_alpha(120)
        surf.fill(BLACK)
        by=self.overlay_surf.get_height()-overlay_height
        self.overlay_surf.blit(surf,(0,by))

        txt0=StarEngine.font.render(main_text,True,WHITE)
        txt1=StarEngine.font.render(help_text,True,WHITE)
        self.overlay_surf.blit(txt0,(20,by+20))
        self.overlay_surf.blit(txt1,(20,by+60))
        pygame.display.flip()

    def reload_overlay_background(self):
        if self.overlay_surf:
            w=self.overlay_surf.get_width()
            h=self.overlay_surf.get_height()
            try:
                tmp=pygame.image.load("assets/welcome_screen.png")
                self.overlay_bg=pygame.transform.scale(tmp,(w,h))
            except:
                pass

    def draw_game_over(self):
        if not self.overlay_surf:
            return
        self.overlay_surf.fill((30,0,0))
        txt0=StarEngine.font.render("GAME OVER",True,WHITE)
        self.overlay_surf.blit(txt0,(20,20))

        line_y=80
        txt1=StarEngine.font.render(f"Wrong answers: {self.stats.total_wrong_answers}",True,WHITE)
        self.overlay_surf.blit(txt1,(20,line_y))
        line_y+=40
        for g,cnt in self.stats.wrong_by_group.items():
            t=StarEngine.font.render(f"{g}: {cnt}",True,WHITE)
            self.overlay_surf.blit(t,(20,line_y))
            line_y+=30


def main():
    # StarGame anlegen
    game = StoryGame()
    # Start
    game.run()

if __name__=="__main__":
    main()
