#!/usr/bin/python2
### Display an animation of vertical bars that either rotate or stream past
### (optic flow illusion).
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

### Usage: './optic_flow.py <mode> <fps>', where
### <mode> is one of ROTATE_RIGHT, ROTATE_LEFT, FLOW_FORWARD, FLOW_BACKWARD
### <fps> is the delay in sec^-1 between screen updates


import arena, shape
import sys, time

### SETTINGS ###

## (Settings may be changed via the commandline, see below.)

# Available animation types and the currently selected mode
global options, mode
options = ("ROTATE_RIGHT", "ROTATE_LEFT", "FLOW_FORWARD", "FLOW_BACKWARD")
mode = "ROTATE_RIGHT"

# Animation speed in frames per second
#XXX doesn't seem to have an effect? -> limited by hardware
global fps
fps = 21

# Foreground and background colour
global fg_col, bg_col
fg_col, bg_col = "blue", "black"

### FUNCTIONS ###

def panel_pattern(x_off):
    global fg_col, bg_col
    "Draw a bar pattern on a single panel with a given offset."
    shape.plot(shape.rectangle(x_off,0, x_off+3,0, x_off+3,arena.height,
                               x_off,arena.height), fg_col)
    shape.plot(shape.rectangle(x_off+4,0, x_off+7,0, x_off+7,arena.height,
                               x_off+4,arena.height), bg_col)
    shape.plot(shape.rectangle(x_off+8,0, x_off+11,0, x_off+11,arena.height,
                               x_off+8,arena.height), fg_col)
    shape.plot(shape.rectangle(x_off+12,0, x_off+15,0, x_off+15,arena.height,
                               x_off+12,arena.height), bg_col)

def rotate(cw=True):
    "Rotate the bar pattern, clockwise (if cw is True) or anticlockwise."
    global fps
    t = 0
    while True:
        if cw: x_offset = t
        else: x_offset = t * (-1)
        panel_pattern(x_offset)
        arena.render()
        time.sleep(1.0/fps)
        if t < 7: t = t+1
        else: t = 0

def flow(fw=True):
    "Show the optic flow pattern, forward (if fw is True) or backward."
    global fps
    t = 0
    while True:
        if fw: x_left, x_right = t*(-1)+4, t
        else: x_left, x_right = t+4, t*(-1)
        panel_pattern(x_right)
        for p in range(8):
            if p < 4: arena.toggle_panel(p, True)
            else: arena.toggle_panel(p, False)
        arena.render()
        panel_pattern(x_left)
        for p in range(8):
            if p < 4: arena.toggle_panel(p, False)
            else: arena.toggle_panel(p, True)
        arena.render()
        time.sleep(1.0/fps)
        if t < 7: t = t+1
        else: t = 0

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
    1st param: animation mode (int or string)
    2nd param: fps
    '''
    global options, mode, fps
    if len(sys.argv) > 4:
        raise Exception("Bad number of args. See the source for details.")
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        if mode.isdigit(): mode = options[int(mode)]
        if mode not in options:
            raise Exception("Invalid mode "+mode+". Must be in "+options)
    if len(sys.argv) == 3:
        fps = int(sys.argv[2])

if __name__ == '__main__':
    parse_args()
    # must run in duplicate mode!
    arena.run(animate, "DUPLICATE")
