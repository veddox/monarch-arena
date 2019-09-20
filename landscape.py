#!/usr/bin/python2
### Display an animation of a landscape with two moving elements.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

import arena, shape
import time

def draw_panorama(col="magenta"):
    "Draw a panorama of two triangular hills"
    arena.clear("blue", show=False)
    panorama = shape.line(0,15,127,15) + \
               shape.triangle(0, 14, 10, 8, 20, 14) + \
               shape.triangle(64, 14, 69, 5, 74, 14)
    shape.plot(panorama, colour=col)

def draw_movable_elements(t, x0_pixel=0, x0_strip=arena.width/2, px_foreground=True):
    '''
    Draw a green pixel and black vertical strip at timestep t.
    The pixel moves clockwise, the strip ACW around the arena.

    x0_pixel, x0_strip: Initial x-coordinates of the elements
    px_foreground: Should the pixel be in the fore- or background?
    '''
    if not px_foreground:
        arena.set_pixel(x0_pixel+t, 6, "green")
    shape.plot(shape.line(x0_strip-t, 3, x0_strip-t, 9), "black")
    if px_foreground:
        arena.set_pixel(x0_pixel+t, 6, "green")

def animate(ticks=-1, fps=21):
    '''
    Animate the elements at the given framerate for a set time
    
    ticks: number of ticks to run the animation for (-1 -> forever)
    fps: framerate in ticks per second (default: 21fps = 60deg/s)
    '''
    i = 0
    while i != ticks:
        i = i + 1 # infinity loop if ticks = -1
        draw_panorama()
        draw_movable_elements(i, px_foreground=True)
        arena.render()
        time.sleep(1.0/fps)   
        
if __name__ == '__main__':
    arena.run(animate, "PARALLEL")
