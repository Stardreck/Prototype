from models.event_card import EventCard
from models.planet import Planet
from models.story import Story


class GameData:
    def __init__(self):
        ##### Planets #####
        planet_dicts = [
            {
                "name": "TerraNova",
                "row": 2,
                "col": 3,
                "visited": False,
                "bg_image": "assets/welcome_screen.jpeg"
            },
            {
                "name": "Mars",
                "row": 4,
                "col": 6,
                "visited": False,
                "isFuelPlanet": True,
                "bg_image": "assets/welcome_screen.jpeg"
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

        ##### Story #####
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

        ##### Events #####
        event_dicts = [
            {
                "name": "Asteroiden-Feld",
                "description": "Jemand hat die Toilette verstopft. Hull -1, Fuel -2",
                "hull_change": -1,
                "fuel_change": -2,
                "image": "assets/event_card.png",
                "type": "negative"
            },
            {
                "name": "Alter Satellit",
                "description": "Treibt im All. Fuel +2",
                "hull_change": 0,
                "fuel_change": 2,
                "image": "assets/event_card.png",
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

        self.event_probability = 1  # how likely it is that an event is triggered

        ##### Quizzes and tasks #####
        # default set is used on empty fields
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