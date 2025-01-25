class EventCard:
    """
    Represents an event card
    """
    def __init__(self, name, description, hull_change=0, fuel_change=0,
                 image=None, event_type="negative"):
        self.name = name
        self.description = description
        self.hull_change = hull_change
        self.fuel_change = fuel_change
        self.image = image
        self.type = event_type