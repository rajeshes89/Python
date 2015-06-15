class A: 
    foo = []
    
a = A()
b = A()
print(a.foo.append(5))
print(b.foo)

class A: 
    def __init__(self): 
        self.foo = []
a = A()
b = A()
print(a.foo.append(5))
print(b.foo)

class temp1:
    def __init__(self,a):
        self.a = a

t1 = temp1(55)

class temp2:
    temp1.__init__(self)

t2 = temp2()
print(t2.a)
