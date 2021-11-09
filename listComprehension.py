#! /usr/bin/python

#Basic list comprehension syntax 

#if condition syntax , [for loop , if <>]
#if else condition syntax , [if <> else <> for loop]

numbers = [1, 12, 37, 43, 51, 62, 83, 43, 90, 2020]

[i for i in numbers if i%2 ==1]
#prints [1, 37, 43, 51, 83, 43]

[i for i in numbers if i%2 ==0]
#prints [12, 62, 90, 2020]

#using lambda 

print(list(filter(lambda x: x % 2 == 1, numbers)))
##prints [1, 37, 43, 51, 83, 43]

#if else in list comprehension

[i if i%2 ==1 else 0 for i in numbers]
## prints [1, 0, 37, 43, 51, 0, 83, 43, 0, 0]
