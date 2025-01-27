class Planet:
    def __init__(self, name, row, col, visited=False, is_fuel_planet=False, background_image=None, cutscene_media=None):
        self.name = name
        self.row = row
        self.col = col
        self.visited = visited
        self.is_fuel_planet = is_fuel_planet
        self.background_image = background_image
        self.cutscene_media = cutscene_media
