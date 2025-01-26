from typing import List, Optional


class Story:
    def __init__(self, title: str, story_lines: List[str], audio_clip: Optional[str] = None):
        self.title = title
        self.story_lines = story_lines
        self.audio_clip = audio_clip
