
class RectangleParticle(Particle):
    """Rectangle shape subclass"""
    def __init__(self, x, y, width, height, color, alpha=1.0):
        super().__init__(x, y, color)

        self.width = width
        self.height = height

    def draw(self):
        """Draw the shape using Kivy canvas instructions"""
        super().draw()

        self.size = (self.width, self.height)

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2], self.color[3] if len(self.color) > 3 else 1)
            self.rect = Rectangle(pos=(self.x, self.y), size=(self.width, self.height))