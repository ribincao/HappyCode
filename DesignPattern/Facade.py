"""
author: ribincao
desc FacadeModel Demo
"""


# System
class Shape:

    def __init__(self):
        pass

    def draw(self):
        pass


class Circle(Shape):

    def __init__(self):
        super(Circle, self).__init__()

    def draw(self):
        print('Draw Circle.')


class Rectangle(Shape):

    def __int__(self):
        super(Rectangle, self).__init__()

    def draw(self):
        print('Draw Rectangle.')


# Facade
class ShapeFacade:

    def __init__(self):
        self.circle = Circle()
        self.rectangle = Rectangle()

    def draw_circle(self):
        self.circle.draw()

    def draw_rectangle(self):
        self.rectangle.draw()


if __name__ == '__main__':
    sf = ShapeFacade()
    sf.draw_circle()
    sf.draw_rectangle()
