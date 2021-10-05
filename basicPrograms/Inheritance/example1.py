class Shape:
    def name(self):
        print("shape")
class Circle(Shape):
    def name(self):
        print("circle")

c = Circle()
s = Shape()
c.name()
s.name()
