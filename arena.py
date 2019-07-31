#!/usr/bin/python2
### Control the LEDs in the ZooII Monarch butterfly arena.
###
### This is a library module that is meant to be imported by experiment scripts.
### It provides functions to initialize the arena, and to draw a variety of
### basic shapes that may be combined as needed. It also offers a simple
### commandline interface to control the arena lights.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the MIT License

import sys, math, copy
import RPi.GPIO as GPIO              #https://pypi.org/project/RPi.GPIO/
from dotstar import Adafruit_DotStar #https://github.com/adafruit/Adafruit_DotStar_Pi

## The mode determines which output device is chosen and how this is treated.
## "TEXT":      Print an ASCII representation to STDOUT (during development)
## "SERIAL":    All arena LEDs arranged serially, legacy mode
## "PARALLEL":  Arena decomposed into 8 subpanels that may be addressed separately
##              for better performance
## "DUPLICATE": All subpanels are sent identical information (limits screen size
##              to 16x16 pixels)
global MODE = "SERIAL"

## RASPBERRY GPIO SETUP
## see https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

if MODE != "TEXT":
    GPIO.cleanup()           #XXX Call this again at the end?
    GPIO.setmode(GPIO.BCM)   #XXX Wouldn't BOARD be better? (higher-level)
    #GPIO.setwarnings(False) #XXX I don't like disabling warnings by default...
    GPIO.setup(25, GPIO.OUT) #select parallel or serial mode

if MODE == "SERIAL":
    GPIO.output(25,GPIO.HIGH)
elif MODE == "PARALLEL" or MODE == "DUPLICATE":
    GPIO.output(25,GPIO.LOW)

## TODO I somehow need to figure out which GPIO pins correspond to which
## panels, so I can switch them on or off as needed
## (duplicate mode -> all panels always on)
    
#TODO The next lines were just copied from Keram...
#GPIOs for stimedent and stimstart/end
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.output(26,GPIO.LOW)
GPIO.output(19,GPIO.LOW)

## LED STRIP SETUP

## Arena dimensions in pixels/LEDs
global height, width, npanels
height = 16
width = 128
npanels = 8

global strip
strip = Adafruit_DotStar(height*width, 2000000)
strip.begin()

global colours
colours = {"red":(strip.Color(0, 15, 0), "R"),
           "green":(strip.Color(1, 0, 0), "G"),
           "blue":(strip.Color(0, 0, 1), "B"),
           "black":(strip.Color(0, 0, 0), "-"),
           "orange":(strip.Color(2,5,0), "O"),
           "magenta":(strip.Color(0, 5, 7), "M"),
           "yellow":(strip.Color(10, 10, 0), "Y"),
           "cyan":(strip.Color(10, 0, 10), "C")}

## ARENA DEFINITIONS

global arena, old_arena
arena = ["black"] * height * width
old_arena = copy.copy(arena)

def clear_arena(colour="black", show=True):
    "Reset the arena to a given colour (default: off)"
    global arena, height, width
    arena = [colour] * height * width
    if show: draw_arena()

def wrap_coords(x, y):
    "If a coordinate is out of bounds, wrap around."
    global height, width
    if y < 0 or y >= height: y = y % height
    if x < 0 or x >= width: x = x % width
    return x, y
    
def pixel_id(x, y, toroidal=True):
    "Get the LED ID of a given set of coordinates"
    #toroidal: if true, treat the display as a torus and wrap around
    global height, width
    if x < 0 or y < 0 or x >= width or y >= height:
        if toroidal: x, y = wrap_coords(x, y)
        else: raise Exception(str(x)+"/"+str(y)+" is out of bounds.")
    if x%2 == 1:
        return (x+1)*height - y - 1
    else: return x*height + y

def pixel(x,y):
    "Get the colour of this pixel."
    global arena
    return arena[pixel_id(x,y)]
    
## DRAWING FUNCTIONS

def set_pixel(x,y,colour):
    "Set the colour of a single pixel."
    global arena
    arena[pixel_id(x,y)] = colour

def draw_arena():
    "Draw the current state of the arena to the device."
    global height, width, colour, strip, arena, old_arena
    #TODO This needs to be changed to accomodate the parallel mode
    for y in range(height):
        for x in range(width):
            colour = pixel(x,y)
            old_colour = old_arena[pixel_id(x,y)]
            if colour != old_colour:
                strip.setPixelColor(pixel_id(x,y), colours[pixel(x,y)][0])
    old_arena = copy.copy(arena)
    strip.show()
    
def print_arena():
    "Print out a text representation of the current state of the arena."
    global height, width, colours
    for y in range(height):
        for x in range(width):
            sys.stdout.write(colours[pixel(x,y)][1])
        sys.stdout.write('\n')
        sys.stdout.flush()

## COMMANDLINE INTERFACE

def parseArgs():
    '''
    A rudimentary commandline interface. Usage:
    ./arena.py clear [colour]
    ./arena.py set <x> <y> <colour>
    Use `--serial` or `--parallel` before the clear/set command to choose a mode.
    '''
    global MODE, colours
    #XXX Is it sensible to set the mode via commandline?
    if "--serial" in sys.argv:
        MODE = "SERIAL"
    elif "--parallel" in sys.argv:
        MODE = "PARALLEL"
    elif "clear" in sys.argv:
        if sys.argv[-1] in colours.keys():
            clear_arena(sys.argv[-1])
        else: clear_arena()
    elif "set" in sys.argv:
        x = sys.argv[-3]
        y = sys.argv[-2]
        c = sys.argv[-1]
        if x.isdigit() and y.isdigit() and c in colours.keys():
            set_pixel(int(x),int(y),c)
        else:
            print "Usage: ./arena.py set <x> <y> <colour>"
            return
    draw_arena()

if __name__ == '__main__':
    parseArgs()
