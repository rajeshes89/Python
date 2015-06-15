class Parent(object):
    def change(self):
        print ("In parent change()")
        
class Child(Parent):
    def change(self):
        print ("In child change()b4 super()")
        super().change()
        print ("In child change()after super()")

p = Parent()
c = Child()

p.change()
c.change()
#======
class Parent(object):

    def altered(self):
        print ("PARENT altered()")

class Child(Parent):

    def altered(self):
        print ("CHILD, BEFORE PARENT altered()")
        super(Child, self).altered()
        print ("CHILD, AFTER PARENT altered()")

dad = Parent()
son = Child()

dad.altered()
son.altered()
