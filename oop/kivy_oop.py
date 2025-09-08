from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.clock import Clock
from kivy.vector import Vector
import random
import math


class Shape(Widget):
    """Base class demonstrating encapsulation and basic OOP principles"""
    
    def __init__(self, x, y, color, **kwargs):
        super().__init__(**kwargs)
        # Private attributes (encapsulation)
        self._x = x
        self._y = y
        self._color = color
        self._velocity = Vector(random.uniform(-2, 2), random.uniform(-2, 2))
        self._size = 30
        
    # Property decorators demonstrate encapsulation
    @property
    def position(self):
        return (self._x, self._y)
    
    @position.setter
    def position(self, value):
        self._x, self._y = value
        self.update_graphics()
    
    def move(self):
        """Update position based on velocity"""
        self._x += self._velocity.x
        self._y += self._velocity.y
        
        # Bounce off walls
        if self._x <= 0 or self._x >= self.parent.width - self._size:
            self._velocity.x *= -1
        if self._y <= 0 or self._y >= self.parent.height - self._size:
            self._velocity.y *= -1
            
        # Keep within bounds
        self._x = max(0, min(self.parent.width - self._size, self._x))
        self._y = max(0, min(self.parent.height - self._size, self._y))
        
        self.update_graphics()
    
    def update_graphics(self):
        """Virtual method to be overridden by subclasses"""
        # Update widget position for collision detection
        self.pos = (self._x, self._y)
        self.size = (self._size, self._size)
        pass
    
    def on_touch_down(self, touch):
        """Handle touch events - demonstrates method overriding"""
        if self.collide_point(*touch.pos):
            self.on_click()
            return True
        return False
    
    def on_click(self):
        """Default click behavior - can be overridden"""
        # Change velocity on click
        self._velocity = Vector(random.uniform(-3, 3), random.uniform(-3, 3))


class Circle(Shape):
    """Circle class demonstrating inheritance"""
    
    def __init__(self, x, y, color=(1, 0, 0, 1), **kwargs):
        super().__init__(x, y, color, **kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Override parent method - demonstrates polymorphism"""
        self.canvas.clear()
        # Update widget position and size for collision detection
        self.pos = (self._x, self._y)
        self.size = (self._size, self._size)
        with self.canvas:
            Color(*self._color)
            self.ellipse = Ellipse(pos=(self._x, self._y), size=(self._size, self._size))
    
    def on_click(self):
        """Override parent behavior - demonstrates polymorphism"""
        super().on_click()
        # Circles grow when clicked
        self._size = min(60, self._size + 5)
        self.update_graphics()


class Square(Shape):
    """Square class demonstrating inheritance"""
    
    def __init__(self, x, y, color=(0, 1, 0, 1), **kwargs):
        super().__init__(x, y, color, **kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Override parent method - demonstrates polymorphism"""
        self.canvas.clear()
        # Update widget position and size for collision detection
        self.pos = (self._x, self._y)
        self.size = (self._size, self._size)
        with self.canvas:
            Color(*self._color)
            self.rect = Rectangle(pos=(self._x, self._y), size=(self._size, self._size))
    
    def on_click(self):
        """Override parent behavior - demonstrates polymorphism"""
        super().on_click()
        # Squares change color when clicked
        self._color = (random.random(), random.random(), random.random(), 1)
        self.update_graphics()


class Triangle(Shape):
    """Triangle class with unique behavior"""
    
    def __init__(self, x, y, color=(0, 0, 1, 1), **kwargs):
        super().__init__(x, y, color, **kwargs)
        self._rotation = 0
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
    
    def move(self):
        """Override move to add rotation"""
        super().move()
        self._rotation += 2
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Triangle drawing using canvas instructions"""
        self.canvas.clear()
        # Update widget position and size for collision detection
        self.pos = (self._x, self._y)
        self.size = (self._size, self._size)
        with self.canvas:
            Color(*self._color)
            # Simple triangle using three rectangles (simplified for demo)
            Rectangle(pos=(self._x + 10, self._y), size=(10, 30))
            Rectangle(pos=(self._x, self._y + 15), size=(30, 10))
            Rectangle(pos=(self._x + 5, self._y + 5), size=(20, 20))
    
    def on_click(self):
        """Triangles spin faster when clicked"""
        super().on_click()
        self._velocity *= 1.5
        print(f"Triangle clicked! Velocity increased: {self._velocity}")


class AnimationCanvas(Widget):
    """Canvas widget that holds and manages all shapes"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shapes = []
    
    def on_touch_down(self, touch):
        """Handle touch events and propagate to shapes"""
        # Try each shape in reverse order (top to bottom)
        for shape in reversed(self.shapes):
            if shape.on_touch_down(touch):
                return True
        return super().on_touch_down(touch)
        
    def add_shape(self, shape_class, count=1):
        """Factory method pattern - creates shapes dynamically"""
        for _ in range(count):
            x = random.randint(50, int(self.width - 100))
            y = random.randint(50, int(self.height - 100))
            
            # Polymorphism in action - same interface, different behaviors
            if shape_class == Circle:
                color = (random.random(), 0.2, 0.2, 1)  # Reddish
            elif shape_class == Square:
                color = (0.2, random.random(), 0.2, 1)  # Greenish
            else:  # Triangle
                color = (0.2, 0.2, random.random(), 1)  # Bluish
                
            shape = shape_class(x, y, color)
            self.shapes.append(shape)
            self.add_widget(shape)
    
    def update_animation(self, dt):
        """Update all shapes - demonstrates polymorphism"""
        for shape in self.shapes:
            shape.move()  # Same method call, different behaviors
    
    def clear_shapes(self):
        """Remove all shapes"""
        for shape in self.shapes[:]:
            self.remove_widget(shape)
        self.shapes.clear()


class OOPLessonApp(App):
    """Main application class"""
    
    def build(self):
        # Main layout
        root = BoxLayout(orientation='vertical')
        
        # Title
        title = Label(
            text='Interactive OOP Lesson with Kivy\n'
                 'Click shapes to see polymorphism in action!\n'
                 'Red Circles: Grow larger | Green Squares: Change color | Blue Triangles: Spin faster',
            size_hint_y=None,
            height=100,
            text_size=(None, None),
            halign='center'
        )
        
        # Animation canvas
        self.canvas = AnimationCanvas()
        
        # Control buttons
        controls = BoxLayout(size_hint_y=None, height=60)
        
        btn_circles = Button(text='Add Circles')
        btn_circles.bind(on_press=lambda x: self.canvas.add_shape(Circle, 3))
        
        btn_squares = Button(text='Add Squares')
        btn_squares.bind(on_press=lambda x: self.canvas.add_shape(Square, 3))
        
        btn_triangles = Button(text='Add Triangles')
        btn_triangles.bind(on_press=lambda x: self.canvas.add_shape(Triangle, 3))
        
        btn_clear = Button(text='Clear All')
        btn_clear.bind(on_press=lambda x: self.canvas.clear_shapes())
        
        btn_info = Button(text='OOP Info')
        btn_info.bind(on_press=self.show_oop_info)
        
        controls.add_widget(btn_circles)
        controls.add_widget(btn_squares)
        controls.add_widget(btn_triangles)
        controls.add_widget(btn_clear)
        controls.add_widget(btn_info)
        
        # Assembly
        root.add_widget(title)
        root.add_widget(self.canvas)
        root.add_widget(controls)
        
        # Start animation
        Clock.schedule_interval(self.canvas.update_animation, 1.0/60.0)
        
        # Add initial shapes
        Clock.schedule_once(self.add_initial_shapes, 0.5)
        
        return root
    
    def add_initial_shapes(self, dt):
        """Add some initial shapes to demonstrate concepts"""
        if self.canvas.width > 0:  # Make sure canvas is ready
            self.canvas.add_shape(Circle, 2)
            self.canvas.add_shape(Square, 2)
            self.canvas.add_shape(Triangle, 2)
    
    def show_oop_info(self, instance):
        """Display OOP concepts demonstrated"""
        print("\n" + "="*50)
        print("OOP CONCEPTS DEMONSTRATED:")
        print("="*50)
        print("1. ENCAPSULATION:")
        print("   - Private attributes (_x, _y, _color)")
        print("   - Property decorators (@property)")
        print("   - Methods that manage internal state")
        print()
        print("2. INHERITANCE:")
        print("   - Shape (base class)")
        print("   - Circle, Square, Triangle (derived classes)")
        print("   - super() calls to parent methods")
        print()
        print("3. POLYMORPHISM:")
        print("   - Same method names, different behaviors")
        print("   - update_graphics() overridden in each shape")
        print("   - on_click() behaves differently per shape")
        print()
        print("4. ABSTRACTION:")
        print("   - Shape class defines common interface")
        print("   - Users don't need to know implementation details")
        print()
        print("Click shapes to see polymorphism in action!")
        print("="*50)


if __name__ == '__main__':
    OOPLessonApp().run()