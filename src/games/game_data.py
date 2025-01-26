import json
from pathlib import Path
from typing import List, Dict, Any

from factories.planet_factory import PlanetFactory
from factories.event_factory import EventFactory
from factories.story_factory import StoryFactory
from models.event_card import EventCard
from star_config import StarConfig
from models.planet import Planet
from models.story import Story



class GameData:
    def __init__(self, config: StarConfig, data_directory: str = "data"):
        self.planet_quizzes = self.load_quizzes(Path(data_directory) / "quizzes.json")
        self.planets = self.load_planets(Path(data_directory) / "planets.json")
        self.story_segments = self.load_stories(Path(data_directory) / "stories.json")
        self.event_cards = self.load_events(Path(data_directory) / "events.json")

        self.event_probability = config.event_probability

    def load_planets(self, path: Path) -> List[Planet]:
        with open(path, "r") as file:
            planet_data = json.load(file)
        return [PlanetFactory.create_planet(planet) for planet in planet_data]

    def load_events(self, path: Path) -> List[EventCard]:
        with open(path, "r") as file:
            event_data = json.load(file)
        return [EventFactory.create_event(event) for event in event_data]

    def load_stories(self, path: Path) -> dict[Any, Story]:
        with open(path, "r", encoding="utf-8") as file:
            story_data = json.load(file)
        return {planet: StoryFactory.create_story(data) for planet, data in story_data.items()}

    def load_quizzes(self, path: Path) -> Dict[str, List[Dict[str, Any]]]:
        with open(path, "r") as file:
            return json.load(file)