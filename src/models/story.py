class Story:
    def __init__(self, lines=None):
        if lines is None:
            lines = []
        self.lines = lines