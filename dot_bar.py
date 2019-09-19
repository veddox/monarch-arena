#!/usr/bin/python2
### Display a simple animation of a vertical bar and a moving green dot.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

import arena, shape
import time

global background
background = "black" #TODO change to "blue" for use in the actual arena

def draw_movable_elements(t, x0_pixel=0, x0_strip=arena.width/2, px_foreground=True):
    '''
    Draw a green pixel and black vertical strip at timestep t.
    The pixel moves clockwise around the arena.

    x0_pixel, x0_strip: Initial x-coordinates of the elements
    px_foreground: Should the pixel be in the fore- or background?
    '''
    global background
    arena.set_pixel(x0_pixel+t-1, 6, background) #delete the last pixel
    if not px_foreground:
        arena.set_pixel(x0_pixel+t, 6, "green")
    shape.plot(shape.line(x0_strip, 0, x0_strip, arena.height), "blue") #TODO change to "black"
    if px_foreground:
        arena.set_pixel(x0_pixel+t, 6, "green")

def animate(ticks=-1, fps=21):
    '''
    Animate the elements at the given framerate for a set time
    
    ticks: number of ticks to run the animation for (-1 -> forever)
    fps: framerate in ticks per second (default: 21fps = 60deg/s)
    '''
    global background
    arena.clear(background, show=False)
    i = 0
    while i != ticks:
        i = i + 1 # infinity loop if ticks = -1
        draw_movable_elements(i, px_foreground=True)
        arena.render()
        time.sleep(1.0/fps)   
        
if __name__ == '__main__':
    arena.run(animate, "TEXT") #TODO change to "PARALLEL"
