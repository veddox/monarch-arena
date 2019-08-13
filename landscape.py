#!/usr/bin/python2
### Display an animation of a landscape with two moving elements.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

import arena
import draw

arena.set_mode("TEXT")     #TODO change to "PARALLEL"
arena.clear_arena("black", show=False) #TODO Change to "blue" for use in the actual arena

#TODO
# - gruener Pixel
# - schwarzer, vertikaler Streifen
# - werden einzeln im Kreis bewegt, mal vor, mal hintereinander
# - 60 deg/s -> 21fps
# - Huegelpanorama

def draw_panorama(col="magenta"):
    "Draw a panorama of two triangular hills"
    #FIXME triangles broken - is `draw.diagonal_line()`buggy?
    panorama = draw.line(0,15,127,15) + \
               draw.triangle(0, 14, 10, 8, 20, 14) + \
               draw.triangle(64, 14, 69, 5, 74, 14)
    draw.shape(panorama, colour=col)


if __name__ == '__main__':
    draw_panorama()
    arena.draw_arena()
