from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle, Triangle
from kivy.clock import Clock
from kivy.vector import Vector
import random
import math

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
        """Draw the shape using Kivy canvas instructions"""
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


class AnimationCanvas(Widget):
    """Canvas to hold and animate shapes"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.particles = []

        for i in range(50):

            radius = random.randint(20, 50)
            w = random.randint(40, 100)
            h = random.randint(20, 80)
            
            x = random.randint(radius, 800 - radius)
            y = random.randint(radius, 600 - radius)
            color = (random.random(), random.random(), random.random(), random.uniform(0.5, 1.0))


            picked_particle = random.choice(range(4))

            if picked_particle == 0:
                self.particles.append(Particle(x, y, color))
                self.add_widget(self.particles[-1])
            
            if picked_particle == 1:
                self.particles.append(CircleParticle(x, y, radius, color))
                self.add_widget(self.particles[-1])

            if picked_particle == 2:
                self.particles.append(RectangleParticle(x, y, w, h, color))
                self.add_widget(self.particles[-1])

            if picked_particle == 3:
                self.particles.append(TriangleParticle(x, y, w, h, color))
                self.add_widget(self.particles[-1])




        
    def draw(self, dt):
        """Draw all shapes"""
        for particle in self.particles:
            particle.update(dt)
            particle.draw()


class OOPLessonApp(App):
    """Main application class"""
    
    def build(self):
        root = BoxLayout(orientation='vertical')
                
        self.canvas = AnimationCanvas()
        root.add_widget(self.canvas)
        
        Clock.schedule_interval(self.canvas.draw, 1.0/60.0)

        return root

    


if __name__ == '__main__':
    OOPLessonApp().run()