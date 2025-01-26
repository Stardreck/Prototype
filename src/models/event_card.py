from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from games.story_game import StoryGame

class EventCard:
    """
    Represents an event card
    """
    def __init__(self, name: str, description: str, hull_change: int = 0, fuel_change: int = 0,
                 image: str = None, event_type: str = "negative", duration: int = 0,
                 repeats: bool = False, required_conditions: dict = None, category: str = None):
        self.name = name
        self.description_template = description  # Speichern der Vorlage
        self.hull_change = hull_change
        self.fuel_change = fuel_change
        self.image = image
        self.type = event_type
        self.duration = duration
        self.repeats = repeats
        self.required_conditions = required_conditions or {}
        self.category = category

    @property
    def description(self) -> str:
        """
        Dynamisch formatierte Beschreibung basierend auf hull_change und fuel_change.

        :return: Formatierte Beschreibung als String.
        """
        return self.description_template.format(
            hull_change=self.hull_change,
            fuel_change=self.fuel_change
        )

    def apply_effect(self, game: StoryGame):
        """
        apply the card effect
        """
        game.fuel += self.fuel_change
        game.hull += self.hull_change
        print(f"[EventCard] apply fuel_change: {self.fuel_change}")
        print(f"[EventCard] apply hull_change: {self.hull_change}")

    def revert_effect(self, game: StoryGame):
        """
        revert the card effect
        """
        game.fuel -= self.fuel_change
        game.hull -= self.hull_change
        print(f"[EventCard] revert fuel_change: {self.fuel_change}")
        print(f"[EventCard] revert hull_change: {self.hull_change}")
