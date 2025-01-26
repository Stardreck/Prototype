# src/factories/event_factory.py

from typing import Dict, Any

from models.story import Story


class StoryFactory:
    @staticmethod
    def create_story(story_data: Dict[str, Any]) -> Story:
        return Story(
            title=story_data.get("title", ""),
            story_lines=story_data.get("story_lines", []),
            audio_clip=story_data.get("audio_clip", None)
        )
