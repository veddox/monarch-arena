#!/usr/bin/python
# A mockup of the dotstar library to allow arena.py to run while not
# on the production system...
# Daniel Vedder

class Adafruit_DotStar():

    def __init__(self, length, hertz):
        pass

    def begin(self):
        pass

    def setPixelColor(self, i, colour):
        print i, colour
    
    def show(self):
        pass

    class Color():
        def __init__(self, r, g, b):
            pass

