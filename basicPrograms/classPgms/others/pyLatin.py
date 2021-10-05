#! /usr/bin/python
import os
import sys

def pyLatin(word):
    word = word.lower()
    return word[1:len(word)] + "ay" + word[0]

print(pyLatin("Python"))
