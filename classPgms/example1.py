#class.py
k = 99
class myClass:
    I = 123
    def function():
        return "hello world"

#x = myClass()
#print(x)
#print(x.I)

class Time:
    k = 00
    def __init__(self):
        self.hour = 0
        self.minute = 0
        self.second = 0
    def printMilitary(self):
        print ("%.2d:%.2d:%.2d" %(self.hour,self.minute,self.second))
