import os

def fibonacci(n):
    first = 0
    second = 1
    next = 0
    for i in range(n):
        print (next)
        next = first + second
        first = second
        second = next
        

print (fibonacci(7))
        
