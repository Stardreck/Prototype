from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from games.story_game import StoryGame

from models.game_object import GameObject


class InventoryManager:
    """
    Manages the player's inventory, handling adding, removing, and listing items.
    """

    def __init__(self, game: StoryGame):
        self.game: StoryGame = game
        self.items: List[GameObject] = []

    def add_item(self, item: GameObject) -> None:
        """
        Adds a GameObject to the inventory.
        """
        self.items.append(item)
        print(f"[InventoryManager] item added: {item.name}")

    def remove_item(self, item: GameObject) -> bool:
        """
        Removes a GameObject from the inventory. Returns True if successful.
        """

        if item in self.items:
            self.items.remove(item)
            print(f"[InventoryManager] item removed: {item.name}")
            return True

        print(f"[InventoryManager] item not found: {item.name}")
        return False

    def get_items(self) -> List[GameObject]:
        """
        Returns a list of all GameObjects in the inventory.
        """
        return self.items

    def find_item_by_name(self, name: str) -> Optional[GameObject]:
        """
        Finds a GameObject in the inventory by its name.
        """
        for item in self.items:
            if item.name == name:
                return item
        return None

    def clear_inventory(self) -> None:
        """
        Removes all items from the inventory.
        """
        self.items.clear()
        print("[InventoryManager] inventory cleared.")