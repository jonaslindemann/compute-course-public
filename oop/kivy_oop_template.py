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


            picked_particle = random.choice(range(1))

            if picked_particle == 0:
                self.particles.append(RectangleParticle(x, y, w, h, color))
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