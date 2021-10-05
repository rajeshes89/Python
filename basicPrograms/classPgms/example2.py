#classExample2.py

from classExample1 import Time
import classExample1

time1 = Time()
print(time1.printMilitary())
time1.hour = 12
time1.printMilitary()
print(time1.k)
time1.k = 100
time1.printMilitary()

