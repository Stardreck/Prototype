import random
import pygame

from typing import List

from models.event_card import EventCard


class EventManager:
    def __init__(self, event_cards: List[EventCard], base_probability: float = 0.3):
        self.negative_events: List[EventCard] = [card for card in event_cards if card.type == "negative"]
        self.positive_events: List[EventCard] = [card for card in event_cards if card.type == "positive"]
        self.error_count: int = 0
        self.max_error: int = 5
        self.event_probability: float = base_probability

        ##### load event card backgrounds #####
        self.event_card_surfaces = {}
        self.__load_event_assets()

    def get_card_surface(self, card_name: str):
        return self.event_card_surfaces.get(card_name, None)

    def increase_error_count(self):
        if self.error_count < self.max_error:
            self.error_count += 1

    def decrease_error_count(self):
        if self.error_count > 0:
            self.error_count -= 1

    def should_trigger_event(self):
        return (random.random() < self.event_probability)

    def pick_event(self):
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

    def __load_event_assets(self):
        """

        """
        for card in self.negative_events + self.positive_events:
            try:
                surf = pygame.image.load(card.image).convert_alpha()
            except:
                surf = pygame.Surface((200, 300))
                surf.fill((150, 0, 150))
            self.event_card_surfaces[card.name] = surf
