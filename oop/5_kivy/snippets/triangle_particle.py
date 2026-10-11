class TriangleParticle(Particle):
    """Triangle shape subclass"""
    def __init__(self, x, y, w, h, color):
        super().__init__(x, y, color)

        self.width = w
        self.height = h


    def draw(self):
        """Draw the shape using Kivy canvas instructions"""
        super().draw()

        self.size = (self.width, self.height)

        with self.canvas:
            Color(self.color[0], self.color[1], self.color[2], self.color[3] if len(self.color) > 3 else 1)
            half_size = self.size[0] / 2
            points = [self.x, self.y + half_size,
                      self.x - half_size, self.y - half_size,
                      self.x + half_size, self.y - half_size]
            self.triangle = Triangle(points=points)
