class Planet:
    def __init__(self, name, row, col, visited=False, is_fuel_planet=False, bg_image=None):
        self.name = name
        self.row = row
        self.col = col
        self.visited = visited
        self.is_fuel_planet = is_fuel_planet
        self.bg_image = bg_image