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
## "SERIAL":    All arena LEDs arranged serially, legacy mode
## "PARALLEL":  Arena decomposed into 8 subpanels that may be addressed separately
##              for better performance
## "DUPLICATE": All subpanels are sent identical information (limits screen size
##              to 16x16 pixels but minimises time delays)
global MODE
MODE = "PARALLEL" #DO NOT CHANGE THIS DIRECTLY! (use `set_mode()` or `run()`)


## RASPBERRY GPIO SETUP
## see https://sourceforge.net/p/raspberry-gpio-python/wiki/BasicUsage/

# The pin used by the hardware to toggle between parallel and serial mode
global toggle
toggle = 25

# The GPIO pin numbers used to activate the eight panels
global pins
pins = (5, 6, 13, 19, 26, 16, 20, 21)

def init_GPIO():
    "(Re)initialise the Raspberry Pi GPIO pins"
    global MODE, toggle, pins
    if MODE == "TEXT": return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(toggle, GPIO.OUT)
    GPIO.output(toggle, GPIO.LOW)
    for p in pins:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, GPIO.LOW)
    # Toggle the hardware mode if necessary
    if MODE == "SERIAL":
        GPIO.output(toggle, GPIO.HIGH)
    # Turn on the panel pins if necessary
    if MODE == "SERIAL" or MODE == "DUPLICATE":
        for p in pins:
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

## SPI clockrate determines data throughput rate from the Pi to the panels
global spi_clock
spi_clock = 10000000 # 10 MHz

## Adafruit strip object and internal representations of the strip buffer
global strip, arena, changed_panels

def init_arena():
    "Create the strip and buffer objects"
    global strip, arena, changed_panels
    global spi_clock, height, pwidth, width, npanels
    strip = Adafruit_DotStar(height*pwidth, spi_clock)
    strip.begin()
    #TODO For maximum speed, use a byte array of RGB values instead
    # (see `image-pov.py` in the Adafruit library for example code)
    arena = ["black"] * height * width
    changed_panels = [False] * npanels

init_arena()

global colours
colours = {"black":(strip.Color(0, 0, 0), "-"),
           "red":(strip.Color(0, 15, 0), "R"),
           "green":(strip.Color(1, 0, 0), "G"),
           "blue":(strip.Color(0, 0, 1), "B"),
           "orange":(strip.Color(2,5,0), "O"),
           "magenta":(strip.Color(0, 5, 7), "M"),
           "yellow":(strip.Color(10, 10, 0), "Y"),
           "cyan":(strip.Color(10, 0, 10), "C")}

## ARENA FUNCTIONS

def clear(colour="black", show=True):
    "Reset the arena to a given colour (default: black/off)"
    global arena, npanels, changed_panels
    for a in range(len(arena)): arena[a] = colour
    changed_panels = [True] * npanels
    if show: render()

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

## PLOTTING FUNCTIONS

def set_pixel(x,y,colour):
    "Set the colour of a single pixel."
    global arena, changed_panels, pwidth, height
    pid = pixel_id(x,y)
    arena[pid] = colour
    #prior to v3, Python doesn't convert to float when dividing ints
    changed_panels[pid/(pwidth*height)] = True
    
def print_arena():
    "Print out a text representation of the current state of the arena."
    global height, width, colours
    for y in range(height):
        for x in range(width):
            sys.stdout.write(colours[pixel(x,y)][1])
        sys.stdout.write('\n')
        sys.stdout.flush()

def render():
    "Output the current state of the arena to the device"
    #TODO needs to be tested
    global MODE, strip, arena, pins, changed_panels
    global height, width, pwidth, colour, npanels
    # text mode is handled by a different function
    if MODE == "TEXT":
        print_arena()
        return
    # update each panel that has been changed
    for p in range(npanels):
        if not changed_panels[p]: continue
        # make sure to activate a panel when in parallel mode
        if MODE == "PARALLEL": GPIO.output(pins[p], GPIO.HIGH)
        for y in range(height):
            for x in range(pwidth):
                pid = pixel_id(x+(p*pwidth), y)
                col = colours[arena[pid]][0]
                spid = pid - (p*pwidth*height)
                strip.setPixelColor(spid, col)
        strip.show()
        if MODE == "PARALLEL": GPIO.output(pins[p], GPIO.LOW)
        changed_panels[p] = False

## UTILITY FUNCTIONS
                
def set_mode(new_mode):
    '''
    Change the output mode to one of 'TEXT', 'SERIAL', 'PARALLEL', 'DUPLICATE'
    Call this instead of setting MODE directly!
    Even better, use `arena.run()` instead.
    '''
    global MODE
    if new_mode not in ("TEXT", "SERIAL", "PARALLEL", "DUPLICATE"):
        raise Exception("Invalid mode "+new_mode)
    else:
        MODE = new_mode
        init_GPIO()
        init_dimensions()
        init_arena()

def toggle_panel(panel, value=None):
    '''
    Turn a panel (0-7) on or off. (value == True -> on, value == False -> off,
    value == None -> toggle). Can only be used in DUPLICATE mode!
    '''
    global MODE, pins
    if MODE != "DUPLICATE":
        raise Exception("Can only toggle panels in DUPLICATE mode.")
    if value == None:
        value = not bool(GPIO.input(panel))
    elif value == True:
        value = GPIO.HIGH
    elif value == False:
        value = GPIO.LOW
    else: raise Exception("Invalid toggle value "+str(value))
    GPIO.output(pins[panel], value)
        
def run(display_fn, mode=None):
    '''
    Execute the function display_fn safely. Strongly recommended for scripts!
    display_fn: A function object to execute (no arguments accepted).
    mode: The mode to switch to before execution.
    '''
    if mode is not None: set_mode(mode)
    try:
        display_fn()
    except KeyboardInterrupt:
        print "Terminating."
    except Exception as e:
        print "Error:", e
    finally:
        GPIO.cleanup()
        
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
            clear(sys.argv[-1])
        else: clear()
    elif "set" in sys.argv:
        x = sys.argv[-3]
        y = sys.argv[-2]
        c = sys.argv[-1]
        if x.isdigit() and y.isdigit() and c in colours.keys():
            set_pixel(int(x),int(y),c)
        else:
            print "Usage: ./arena.py set <x> <y> <colour>"
            return
    render()
    GPIO.cleanup()

if __name__ == '__main__':
    parseArgs()
