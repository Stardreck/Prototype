import pyglet

class Scene:
    def __init__(self, id, game_id, background, text):
        self.id = id
        self.game_id = game_id
        self.background_path = background
        self.text = text
        self.background = None

    def load_assets(self):
        try:
            self.background = pyglet.resource.image(self.background_path)
        except pyglet.resource.ResourceNotFoundException:
            print(f"Background image {self.background_path} not found.")

    def render(self, window):
        if self.background:
            self.background.blit(0, 0)
        label = pyglet.text.Label(
            self.text,
            font_name='Arial',
            font_size=20,
            x=window.width // 2,
            y=window.height // 2,
            width=window.width - 40,
            multiline=True,
            anchor_x='center',
            anchor_y='center'
        )
        label.draw()
