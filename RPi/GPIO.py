#!/usr/bin/python
# A mockup of the RPi.GPIO library to allow arena.py to run while not actually
# on a Raspberry Pi...
# Daniel Vedder, August 2019

global BCM, BOARD
BCM = 0
BOARD = 1

global LOW, HIGH
LOW = 0
HIGH = 1

global IN,OUT
IN = 0
OUT = 1

def setmode(mode):
    pass

def cleanup():
    pass

def setup(pin, direction):
    pass

def input(pin):
    return 0

def output(pin, data):
    pass

def gpio_func(pin):
    global IN
    return IN
