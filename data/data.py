# data.py
"""
Hält alle Daten (Planeten, Story, Tasks, Quiz, Events usw.).
"""

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
