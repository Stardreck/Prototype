from __future__ import annotations
import random

from typing import Optional, List, Dict, TYPE_CHECKING
from models.event_card import EventCard

if TYPE_CHECKING:
    from games.story_game import StoryGame


class EventSelectionManager:
    """
    Responsible for selecting events based on probabilities and game state.
    """

    def __init__(self, game: StoryGame, negative_events: List[EventCard], positive_events: List[EventCard],
                 base_probability: float = 0.3, max_error: int = 5):
        self.game = game
        self.negative_events = negative_events
        self.positive_events = positive_events
        self.base_probability = base_probability
        self.error_count = 0
        self.max_error = max_error

    def set_error_count(self, error_count: int):
        self.error_count = error_count

    def calculate_event_probability(self) -> float:
        """Calculate the probability of triggering an event based on error count."""
        return self.base_probability + (0.05 * self.error_count)

    def should_trigger_event(self) -> bool:
        """Determine if an event should be triggered."""
        return random.random() < self.calculate_event_probability()

    def pick_event(self) -> Optional[EventCard]:
        """
        Select an event based on current error count and conditions.
        :return: Selected EventCard or None.
        """
        neg_chance = 0.3 + (0.6 * (self.error_count / self.max_error))  # [0.3..0.9]
        if random.random() < neg_chance and self.negative_events:
            selected_event = random.choice(self.negative_events)
            if self.__check_conditions(selected_event):
                return selected_event
        elif self.positive_events:
            selected_event = random.choice(self.positive_events)
            if self.__check_conditions(selected_event):
                return selected_event
        return None

    def check_for_forced_events(self) -> EventCard | None:
        """
        Check if an event meets the condition (like game_over) and must be forced
        """
        all_events = self.negative_events + self.positive_events

        for event in all_events:

            if event.category == "game_over":
                # check if a game_over condition is met
                if self.__check_conditions(event):
                    return event

        return None

    def __check_conditions(self, event_card: EventCard) -> bool:
        """
        Check if the event meets the required conditions.
        :param event_card: The EventCard to check.
        :return: True if conditions are met, False otherwise.
        """
        if len(event_card.required_conditions.items()) == 0:
            return True

        for key, value in event_card.required_conditions.items():
            if key == "min_fuel" and self.game.fuel > value:
                return True
            if key == "min_hull" and self.game.hull > value:
                return True
            if key == "quiz_error_count" and self.error_count >= value:
                return True
            # Add more conditions as needed
        return False

    def apply_event_scaling(self, event_card: EventCard):
        """
        Scale the effects of a negative event based on error count.

        :param event_card: The EventCard to scale.
        """
        if event_card.type == "negative":
            scale_factor = 1.0 + (self.error_count * 0.5)
            if event_card.hull_change < 0:
                event_card.hull_change = int(event_card.hull_change * scale_factor)
            if event_card.fuel_change < 0:
                event_card.fuel_change = int(event_card.fuel_change * scale_factor)
