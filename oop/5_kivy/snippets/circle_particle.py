
class CircleParticle(Particle):
    """Circle shape subclass"""
    def __init__(self, x, y, radius, color, alpha=1.0):
        super().__init__(x, y, color)

        self.radius = radius

    def draw(self):
        """Draw the shape using Kivy canvas instructions"""
        super().draw()

        self.size = (2*self.radius, 2*self.radius)

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2], self.color[3] if len(self.color) > 3 else 1)
            self.ellipse = Ellipse(pos=(self.x, self.y), size=(self.radius*2, self.radius*2))