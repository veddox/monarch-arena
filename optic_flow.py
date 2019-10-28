#!/usr/bin/python2
### Display an animation of vertical bars that either rotate or stream past
### (optic flow illusion).
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

### Usage: './optic_flow.py <mode> <fps> <duration> <colour> <fast>', where
### <mode> is one of ROTATE_RIGHT, ROTATE_LEFT, FLOW_FORWARD, FLOW_BACKWARD
### <fps> the frames per second for the animation
### <duration> is the number of updates to run the animation for
### <colour> is the foreground colour to use (see arena.py for options)
### <fast> if this is "fast" or "true", turn on fast rotation (see below)


import arena, shape
import sys, time

### SETTINGS ###

## (Settings may be changed via the commandline, see below.)

# Available animation types and the currently selected mode
global options, mode
options = ("ROTATE_RIGHT", "ROTATE_LEFT", "FLOW_FORWARD", "FLOW_BACKWARD")
mode = "ROTATE_RIGHT"

# Animation speed in frames per second
# NOTE: this cannot be sensibly increased _ad infinitum_.
# For rotation with `fast`, the maximum value is around 200 (-> 24Hz),
# for all other settings, the max is around 100 (-> 12Hz).
global fps
fps = 21

# Number of ticks to update (duration < 0 -> forever)
global duration
duration = -1 #default -1

# Foreground and background colour
global fg_col, bg_col
fg_col, bg_col = "green", "black"

# Optimise for speed in rotate(), ignoring possibly dodgy panels
# (see explanation in rotate() for more details)
global fast
fast = False

### FUNCTIONS ###

def panel_pattern(x_off):
    global fg_col, bg_col
    "Draw a bar pattern on a single panel with a given offset."
    global fg_col, bg_col
    col = fg_col
    for x in range(arena.pwidth):
        shape.plot(shape.vline(x+x_off), col)
        if x == 3 or x == 11: col = bg_col
        elif x == 7: col = fg_col

def rotate(cw=True):
    "Rotate the bar pattern, clockwise (if cw is True) or anticlockwise."
    global fps, duration, fast
    t,i = 0,0
    while i != duration:
        p1 = time.time() # time measuring point 1
        if cw: x_offset = t
        else: x_offset = t * (-1)
        panel_pattern(x_offset)
        # Theoretically, the arena should be able to render all eight
        # panels simultaneously. However, on at least one arena, one panel
        # develops problems with this approach. Therefore, I here revert to
        # only updating half the panels at once. If speed is off the essence,
        # this behaviour can be turned off using the `fast` flag.
        if not fast:
            for p in range(8):
                if p < 4: arena.toggle_panel(p, True)
                else: arena.toggle_panel(p, False)
            arena.render()
            panel_pattern(x_offset)
            for p in range(8):
                if p < 4: arena.toggle_panel(p, False)
                else: arena.toggle_panel(p, True)
        arena.render()
        p2 = time.time() # time measuring point 2
        sleep_time = (1.0/fps) - (p2-p1)
        if sleep_time > 0: time.sleep(sleep_time)
        if t < 7: t = t+1
        else: t = 0
        i = i + 1

def flow(fw=True):
    "Show the optic flow pattern, forward (if fw is True) or backward."
    global fps, duration
    t,i = 0,0
    while i != duration:
        p1 = time.time() # time measuring point 1
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
        p2 = time.time() # time measuring point 2
        sleep_time = (1.0/fps) - (p2-p1)
        if sleep_time > 0: time.sleep(sleep_time)
        if t < 7: t = t+1
        else: t = 0
        i = i + 1

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
    3rd param: duration
    4th param: colour
    5th param: fast mode
    '''
    global options, mode, fps, duration, fg_col, fast
    if len(sys.argv) > 6:
        raise Exception("Bad number of args. See the source for details.")
    if len(sys.argv) >= 2:
        mode = sys.argv[1]
        if mode.isdigit(): mode = options[int(mode)]
        if mode not in options:
            raise Exception("Invalid mode "+mode+". Must be in "+options)
    if len(sys.argv) >= 3:
        fps = int(sys.argv[2])
    if len(sys.argv) >= 4:
        duration = int(sys.argv[3])
    if len(sys.argv) >= 5:
        fg_col = sys.argv[4]
    if len(sys.argv) >= 6:
        if sys.argv[5] in ("fast", "True", "true", "TRUE"):
            fast = True

if __name__ == '__main__':
    parse_args()
    print("Running "+mode+" for "+str(duration)+" updates @ "+str(fps)+" fps.")
    # must run in duplicate mode!
    arena.run(animate, "DUPLICATE")
