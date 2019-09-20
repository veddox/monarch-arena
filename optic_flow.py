#!/usr/bin/python2
### Display an animation of vertical bars that either rotate or stream past
### (optic flow illusion).
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

import arena, shape
import sys, time


### SETTINGS ###

## (Settings may be changed via the commandline, see below.)

# Available animation types and the currently selected mode
global options, mode
options = ("ROTATE_RIGHT", "ROTATE_LEFT", "FLOW_FORWARD", "FLOW_BACKWARD")
mode = "ROTATE_RIGHT"

global display_mode
display_mode = "TEXT" #TODO change to "PARALLEL"

# Animation speed in frames per second
global fps
fps = 21

# Foreground and background colour
global fg_col, bg_col
fg_col, bg_col = "blue", "black"

### FUNCTIONS ###

def rotate(cw=True):
    "Rotate the bar pattern, clockwise (if cw is True) or anticlockwise."
    global display_mode, fg_col, bg_col, fps
    if display_mode != "TEXT": arena.set_mode("DUPLICATE") #for efficiency
    t = 0
    while True:
        if cw: x = t
        else: x = t*-1
        shape.plot(shape.rectangle(x,0,x+3,0,x+3,arena.height,
                                   x,arena.height), fg_col)
        shape.plot(shape.rectangle(x+4,0,x+7,0,x+7,arena.height,
                                   x+4,arena.height), bg_col)
        shape.plot(shape.rectangle(x+8,0,x+11,0,x+11,arena.height,
                                   x+8,arena.height), fg_col)
        shape.plot(shape.rectangle(x+12,0,x+15,0,x+15,arena.height,
                                   x+12,arena.height), bg_col)
        arena.render()
        time.sleep(1.0/fps)
        if t < 4: t = t+1
        else: t = 0

def flow(fw=True):
    "Show the optic flow pattern, forward (if fw is True) or backward."
    pass #TODO

def animate():
    "Run the animation chosen by `mode`."
    global mode
    if mode == "ROTATE_RIGHT":
        rotate(True)
    elif mode == "ROTATE_LEFT":
        rotate(False)
    elif mode == "FLOW_FORWARD":
        flow(True)
    elif mode == "FLOW_BACKWARD":
        flow(False)
    else:
        raise Exception("Invalid mode "+mode)

def parse_args():
    '''
    Set parameters from the commandline by argument index.
    1st param: mode (int or string)
    2nd param: display_mode
    3rd param: fps
    '''
    global options, mode, display_mode, fps
    if len(sys.argv) > 4:
        raise Exception("Bad number of args. See the source for details.")
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        if mode.isdigit(): mode = options[int(mode)]
        if mode not in options:
            raise Exception("Invalid mode "+mode+". Must be in "+options)
    if len(sys.argv) >= 3:
        display_mode = sys.argv[2]
    if len(sys.argv) == 4:
        fps = int(sys.argv[3])

if __name__ == '__main__':
    parse_args()
    arena.run(animate, display_mode)
