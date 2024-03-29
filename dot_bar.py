#!/usr/bin/python2
### Display a simple animation of a vertical bar and a moving dot.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

### Usage: './dot_bar.py <dot_mode> <bar_mode> <display_mode> <fps>', where
### <dot_mode> and <bar_mode> are 0 (not shown), 1 (stationary), or 2 (moving)
### <display_mode> is TEXT or PARALLEL
### <fps> is the delay in sec^-1 between screen updates


import arena, shape
import sys, time

### SETTINGS ###

## (Settings may be changed via the commandline, see below.)

# [dot,bar]_mode:
# 0 -> shape is excluded
# 1 -> shape is stationary
# 2 -> shape moves
global dot_mode, bar_mode
dot_mode = 2
bar_mode = 1

global display_mode
display_mode = "PARALLEL"

# Background, bar, and dot colours
global bg_col, bar_col, dot_col
dot_col = "green"
if display_mode == "TEXT":
    bg_col = "black"
    bar_col = "blue"
else:
    bg_col = "blue"
    bar_col = "black"

# Animation speed in frames per second
global fps
fps = 21
    

### FUNCTIONS ###

def draw_bar(t, x0_bar=arena.width/2):
    "Draw the bar at timestep t."
    global bar_mode, bg_col, bar_col
    if bar_mode == 0: return
    elif bar_mode == 1:
        shape.plot(shape.line(x0_bar, 0, x0_bar, arena.height), bar_col)
    elif bar_mode == 2:
        shape.plot(shape.line(x0_bar+t-1, 0, x0_bar+t-1, arena.height), bg_col)
        shape.plot(shape.line(x0_bar+t, 0, x0_bar+t, arena.height), bar_col)
    else:
        raise Exception("Invalid bar mode: "+str(bar_mode))

def draw_dot(t, x0_dot=0, y_dot=6):
    "Draw the dot at timestep t."
    global dot_mode, bg_col, dot_col
    if dot_mode == 0: return
    elif dot_mode == 1:
        arena.set_pixel(x0_dot, y_dot, dot_col)
    elif dot_mode == 2:
        arena.set_pixel(x0_dot-t+1, y_dot, bg_col)
        arena.set_pixel(x0_dot-t, y_dot, dot_col)
    else:
        raise Exception("Invalid dot mode: "+str(dot_mode))

def animate(ticks=-1):
    '''
    Animate the elements at the given framerate for a set time
    
    ticks: number of ticks to run the animation for (-1 -> forever)
    fps: framerate in ticks per second (default: 21fps = 60deg/s)
    '''
    global bg_col, fps
    arena.clear(bg_col, show=False)
    i = 0
    while i != ticks:
        i = i + 1 # infinity loop if ticks = -1
        draw_bar(i)
        draw_dot(i)
        arena.render()
        time.sleep(1.0/fps)   

def parse_args():
    '''
    Set parameters from the commandline by argument index.
    1st param: dot_mode
    2nd param: bar_mode
    3rd param: display_mode
    4th param: fps
    '''
    global dot_mode, bar_mode, display_mode, bg_col, bar_col, fps
    if len(sys.argv) == 2 or len(sys.argv) > 5:
        raise Exception("Bad number of args. See the source for details.")
    if len(sys.argv) >= 3:
        dot_mode = int(sys.argv[1])
        bar_mode = int(sys.argv[2])
    if len(sys.argv) >= 4:
        display_mode = sys.argv[3]
        if display_mode == "TEXT":
            bg_col, bar_col = "black", "blue"
        else:
            bg_col, bar_col = "blue", "black"
    if len(sys.argv) == 5:
        fps = int(sys.argv[4])
    
        
if __name__ == '__main__':
    parse_args()
    arena.run(animate, display_mode)
