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
### Licensed under the terms of the GNU GPLv3

import sys, copy
import RPi.GPIO as GPIO              #https://pypi.org/project/RPi.GPIO/
from dotstar import Adafruit_DotStar #https://github.com/adafruit/Adafruit_DotStar_Pi

## The mode determines which output device is chosen and how this is treated.
## "TEXT":      Print an ASCII representation to STDOUT (during development)
## "SERIAL":    All arena LEDs arranged serially, legacy default mode
## "PARALLEL":  Arena decomposed into 8 subpanels that may be addressed separately
##              for better performance
## "DUPLICATE": All subpanels are sent identical information (limits screen size
##              to 16x16 pixels but minimises time delays)
global MODE
MODE = "SERIAL" #DO NOT CHANGE THIS DIRECTLY! (use `set_mode()`)


## RASPBERRY GPIO SETUP
## see https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

# The pin used by the hardware to toggle between parallel and serial mode
global toggle
toggle = 25

# The GPIO data & clock pin numbers used by the eight panels

# FIXME Problem: the arena only has a single data/clock channel duo. Ergo, we
# can only have a single Dotstar strip. So I basically need to rewrite the
# entire architecture here...

global panels
panels = (5, 6, 13, 19, 26, 16, 20, 21)

def init_GPIO():
    "(Re)initialise the Raspberry Pi GPIO pins"
    global MODE, toggle, panels
    if MODE == "TEXT": return
    GPIO.setmode(GPIO.BCM)   #XXX Wouldn't BOARD be better? (higher-level)
    for p in panels:
        #make sure we're starting with a blank slate
        if GPIO.gpio_func(p) != GPIO.IN:
            GPIO.cleanup()   #XXX Call this again at the end?
            break
    #GPIO.setwarnings(False) #XXX I don't like disabling warnings by default...
    GPIO.setup(toggle, GPIO.OUT) #used to select parallel or serial mode
    GPIO.output(toggle, GPIO.LOW)
    for p in panels:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    # Toggle the hardware mode if necessary
    if MODE == "SERIAL":
        GPIO.output(toggle, GPIO.HIGH)
    # Turn on the panel pins if necessary
    if MODE == "SERIAL" or MODE == "DUPLICATE":
        for p in panels:
            GPIO.output(p, GPIO.HIGH)

init_GPIO() #should be initialised when module first loads

## LED STRIP SETUP

## Arena dimensions in pixels/LEDs
global height, width, pwidth, npanels

def init_dimensions():
    "(Re)define the arena dimensions, depending on the mode"
    global height, width, pwidth, npanels
    # defaults
    height = 16
    pwidth = 16 # panel width
    npanels = 8
    # special cases
    if MODE == "SERIAL" or MODE == "DUPLICATE":
        if MODE == "SERIAL":
            pwidth = pwidth * npanels
        npanels = 1
    # total width
    width = pwidth * npanels

init_dimensions()
    
## Create an Adafruit strip object to interface with the panels
global strip
strip = Adafruit_DotStar(height*pwidth, 2000000) # 2MHz
strip.begin()

global colours
colours = {"black":(strips[0].Color(0, 0, 0), "-"),
           "red":(strips[0].Color(0, 15, 0), "R"),
           "green":(strips[0].Color(1, 0, 0), "G"),
           "blue":(strips[0].Color(0, 0, 1), "B"),
           "orange":(strips[0].Color(2,5,0), "O"),
           "magenta":(strips[0].Color(0, 5, 7), "M"),
           "yellow":(strips[0].Color(10, 10, 0), "Y"),
           "cyan":(strips[0].Color(10, 0, 10), "C")}


## ARENA DEFINITIONS

global arena, old_arena
#XXX change arena to an array of ints to save space?
arena = ["black"] * height * width
old_arena = copy.copy(arena)

def clear_arena(colour="black", show=True):
    "Reset the arena to a given colour (default: black/off)"
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
    "Output the current state of the arena"
    global MODE
    if MODE == "TEXT":
        print_arena()
    elif MODE == "SERIAL":
        draw_arena_serial()
    elif MODE == "PARALLEL":
        draw_arena_parallel()
    elif MODE == "DUPLICATE":
        draw_arena_duplicate()
    
def print_arena():
    "Print out a text representation of the current state of the arena."
    global height, width, colours
    for y in range(height):
        for x in range(width):
            sys.stdout.write(colours[pixel(x,y)][1])
        sys.stdout.write('\n')
        sys.stdout.flush()

def draw_arena_serial():
    "Draw the current state of the arena to the device in serial mode"
    global height, width, colour, strip, arena, old_arena
    for y in range(height):
        for x in range(width):
            colour = pixel(x,y)
            old_colour = old_arena[pixel_id(x,y)]
            if colour != old_colour:
                strip.setPixelColor(pixel_id(x,y), colours[pixel(x,y)][0])
    old_arena = copy.copy(arena)
    strip.show()

def draw_arena_parallel():
    "Draw the arena, taking advantage of the parallel mode"
    #TODO needs to be tested
    global height, width, pwidth, npanels, colour, strip, arena, old_arena
    changed_panels = [False] * npanels
    #FIXME only one panel!
    panel = 0
    for x in range(width):
        if x > 0 and x%pwidth == 0:
            panel = panel + 1
        for y in range(height):
            colour = pixel(x,y)
            old_colour = old_arena[pixel_id(x,y)]
            if colour != old_colour:
                strips[panel].setPixelColor(pixel_id(x%pwidth,y),
                                            colours[pixel(x,y)][0])
                changed_panels[panel] = True
    old_arena = copy.copy(arena)
    # only update panels that have actually changed
    for p in range(len(changed_panels)):
        if changed_panels[p]: strips[p].show()

def draw_arena_duplicate():
    "Draw the current state of the arena, with all panels showing the same"
    #TODO needs to be tested
    global height, width, colour, strips, arena, old_arena
    for y in range(height):
        for x in range(width):
            colour = pixel(x,y)
            old_colour = old_arena[pixel_id(x,y)]
            if colour != old_colour:
                for s in strips:
                    s.setPixelColor(pixel_id(x,y), colours[pixel(x,y)][0])
    old_arena = copy.copy(arena)
    for s in strips:
        s.show()


## UTILITY FUNCTIONS
                
def set_mode(new_mode):
    "Change the output mode to one of 'TEXT', 'SERIAL', 'PARALLEL', 'DUPLICATE'"
    #NB: Call this instead of setting MODE directly!
    global MODE
    if new_mode not in ("TEXT", "SERIAL", "PARALLEL", "DUPLICATE"):
        raise Exception("Invalid mode "+new_mode)
    else:
        MODE = new_mode
        init_GPIO()
        init_dimensions()

def parseArgs():
    '''
    A rudimentary commandline interface. Usage:
    ./arena.py clear [colour]
    ./arena.py set <x> <y> <colour>
    '''
    global MODE, colours
    if "--help" in sys.argv:
        print "Usage:"
        print "\t./arena.py clear [colour]"
        print "\t./arena.py set <x> <y> <colour>"
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
