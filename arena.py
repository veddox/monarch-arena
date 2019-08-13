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

import sys, copy
import RPi.GPIO as GPIO              #https://pypi.org/project/RPi.GPIO/
from dotstar import Adafruit_DotStar #https://github.com/adafruit/Adafruit_DotStar_Pi

## The mode determines which output device is chosen and how this is treated.
## "TEXT":      Print an ASCII representation to STDOUT (during development)
## "SERIAL":    All arena LEDs arranged serially, legacy mode
## "PARALLEL":  Arena decomposed into 8 subpanels that may be addressed separately
##              for better performance
## "DUPLICATE": All subpanels are sent identical information (limits screen size
##              to 16x16 pixels but minimises time delays)
global MODE
MODE = "SERIAL" #for backward compatibility; PARALLEL would be a more sensible default


## RASPBERRY GPIO SETUP
## see https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

# The pin used by the hardware to toggle between parallel and serial mode
global toggle
toggle = 25

# The GPIO data & clock pin numbers used by the eight panels
#FIXME find out clock pin numbers

#XXX I'm not sure I've understood this correctly. Are the pins given in `panels`
# merely used to turn an individual panel on/off? Or are they also the output
# pins needed by the Adafruit library? If the former, I need a whole other
# set of pin numbers to initialise the Adafruit strips, as well as still needing
# the clock pins...

global panels, clock_pins
panels = (5, 6, 13, 19, 26, 16, 20, 21)
clock_pins = (0, 0, 0, 0, 0, 0, 0, 0)

def init_GPIO():
    "(Re)initialise the Raspberry Pi GPIO pins"
    global MODE, toggle, panels, clock_pins
    if MODE == "TEXT": return
    pins = panels + clock_pins
    GPIO.setmode(GPIO.BCM)   #XXX Wouldn't BOARD be better? (higher-level)
    for p in pins:
        #make sure we're starting with a blank slate
        if GPIO.gpio_func(p) != GPIO.IN:
            GPIO.cleanup()   #XXX Call this again at the end?
            break
    #GPIO.setwarnings(False) #XXX I don't like disabling warnings by default...
    GPIO.setup(toggle, GPIO.OUT) #used to select parallel or serial mode
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    # Toggle the hardware mode
    if MODE == "SERIAL":
        GPIO.output(toggle, GPIO.HIGH)
    elif MODE == "PARALLEL" or MODE == "DUPLICATE":
        GPIO.output(toggle, GPIO.LOW)
    # Set up the panel pins
    if MODE == "SERIAL" or MODE == "DUPLICATE":
        for p in panels:
            GPIO.output(p, GPIO.HIGH)

init_GPIO() #should be initialised when module first loads
                
def set_mode(new_mode):
    "Change the output mode to one of 'TEXT', 'SERIAL', 'PARALLEL', 'DUPLICATE'"
    global MODE
    if new_mode not in ("TEXT", "SERIAL", "PARALLEL", "DUPLICATE"):
        raise Exception("Invalid mode "+new_mode)
    else:
        MODE = new_mode
        init_GPIO()

## LED STRIP SETUP

## Arena dimensions in pixels/LEDs
global height, width, pwidth, npanels

height = 16
pwidth = 16 # panel width

if MODE == "SERIAL": npanels = 1
else: npanels = 8

if MODE == "DUPLICATE": width = pwidth
else: width = pwdith*npanels

## Create an Adafruit strip object for each panel
global strips
for s in range(npanels):
    strips.append(Adafruit_DotStar(height*pwidth,
                                   panels[s], clock_pins[s],
                                   2000000)) # 2MHz
    strips[s].begin()

global colours
colours = {"black":(strip.Color(0, 0, 0), "-"),
           "red":(strip.Color(0, 15, 0), "R"),
           "green":(strip.Color(1, 0, 0), "G"),
           "blue":(strip.Color(0, 0, 1), "B"),
           "orange":(strip.Color(2,5,0), "O"),
           "magenta":(strip.Color(0, 5, 7), "M"),
           "yellow":(strip.Color(10, 10, 0), "Y"),
           "cyan":(strip.Color(10, 0, 10), "C")}


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
    global height, width, colour, strips, arena, old_arena
    for y in range(height):
        for x in range(width):
            colour = pixel(x,y)
            old_colour = old_arena[pixel_id(x,y)]
            if colour != old_colour:
                strips[0].setPixelColor(pixel_id(x,y), colours[pixel(x,y)][0])
    old_arena = copy.copy(arena)
    strips[0].show()

def draw_arena_parallel():
    #TODO
    pass

def draw_arena_duplicate():
    #TODO
    pass


## COMMANDLINE INTERFACE

def parseArgs():
    '''
    A rudimentary commandline interface. Usage:
    ./arena.py clear [colour]
    ./arena.py set <x> <y> <colour>
    Use `--serial` or `--parallel` before the clear/set command to choose a mode.
    '''
    global MODE, colours
    #FIXME change mode selectors to `--mode <m>` format
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
