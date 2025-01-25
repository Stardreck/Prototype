import random

from models.event_card import EventCard


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
