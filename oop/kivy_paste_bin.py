

class Particle(Widget):
    """Base class for shapes demonstrating encapsulation and inheritance"""

    def __init__(self, x, y, color):
        super().__init__()

        self.x = x
        self.y = y
        self.color = color
        self.velocity = Vector(random.uniform(-100, 100), random.uniform(-100, 100))

    def update(self, dt=1/60):
        """Update circle position"""

        self.x += self.velocity.x * dt
        self.y += self.velocity.y * dt

        # Bounce off walls
        if self.x < 0 or self.x + self.size[0] > 800:
            self.velocity.x *= -1
        if self.y < 0 or self.y + self.size[1] > 600:
            self.velocity.y *= -1

    def draw(self):
        self.canvas.clear()   
        self.pos = (self.x, self.y)

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