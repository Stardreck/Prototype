from typing import Optional

class GameObject:
    """
    Represents an object in the game's inventory.
    """

    def __init__(self, name: str, alias: str, description: str, image_path: Optional[str] = None):
        self.name = name
        self.alias = alias
        self.description = description
        self.image_path = image_path  # Pfad zum Bild des Objekts