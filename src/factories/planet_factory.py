# src/factories/event_factory.py

from typing import Dict, Any

from models.planet import Planet


class PlanetFactory:
    @staticmethod
    def create_planet(planet_data: Dict[str, Any]) -> Planet:
        return Planet(
            name=planet_data["name"],
            row=planet_data["row"],
            col=planet_data["col"],
            visited=planet_data.get("visited", False),
            is_fuel_planet=planet_data.get("isFuelPlanet", False),
            bg_image=planet_data.get("bg_image")
        )
