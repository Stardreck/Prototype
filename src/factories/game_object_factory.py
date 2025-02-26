from typing import Dict, Any

from models.game_object import GameObject


class GameObjectFactory:
    @staticmethod
    def create_game_object(game_object_data: Dict[str, Any]) -> GameObject:
        return GameObject(
            name=game_object_data["name"],
            alias=game_object_data["alias"],
            description=game_object_data["description"],
            image_path=game_object_data["image_path"]
        )