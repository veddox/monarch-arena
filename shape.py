#!/usr/bin/python2
### Control the LEDs in the ZooII Monarch butterfly arena.
###
### This is a library module that is meant to be imported by experiment scripts.
### It extends the core functions in arena.py with a set of shape drawing and
### animation functions.
###
### Daniel Vedder, 2018-2019 <daniel.vedder@stud-mail.uni-wuerzburg.de>
### University of Wuerzburg, Center for Computational and Theoretical Biology
### Licensed under the terms of the GNU GPLv3

import math
import arena

def plot(coords, colour="green", flush=False):
    '''
    Draw a shape from a list of coordinates (as produced by the shape functions).
    colour: The colour to use
    flush: If true, will output the result immediately
    '''
    for c in coords:
        arena.set_pixel(c[0], c[1], colour)
    if flush: arena.render()

## SHAPE DEFINITIONS
## A shape is a list of coordinate tuples whose pixels are to be drawn

def hline(x1, x2, y):
    "A horizontal line from x1/y to x2/y"
    shape = []
    if x2 < x1: x2,x1 = x1,x2
    for x in range(x1, x2+1):
        shape.append((x,y))
    return shape

def vline(x, y1, y2):
    "A vertical line from x/y1 to x/y2"
    shape = []
    if y2 < y1: y2,y1 = y1,y2
    for y in range(y1, y2+1):
        shape.append((x,y))
    return shape

def line(x1, y1, x2, y2):
    "A straight line from x1/y1 to x2/y2"
    # Special cases for improved performance
    if x1 == x2: return vline(x1, y1, y2)
    if y1 == y2: return hline(x1, x2, y1)
    # This is a backport to Python from my Common Lisp croatoan `shapes` extension
    # (https://github.com/McParen/croatoan/blob/master/source/shape.lisp)
    # The idea is to move from left to right one step at a time, calculating how
    # many pixels we need to stack vertically at each position to get a
    # "straight line"
    #FIXME does the line end up being too long?
    shape = []
    # make sure we're moving from left to right
    if x1 > x2 or (x1 == x2 and y1 > y2):
        x1,x2 = x2,x1
        y1,y2 = y2,y1
    # The slope (dy/dx) gives the vertical pixels per x-position
    if x1 == x2:
        slope = abs(y1 - y2) #prevent division-by-zero errors
    else: slope = float(y2-y1) / float(x2-x1)
    # x and y are the distance from the origin (x1/y1), dy is the number of
    # pixels to stack here, and next_x/next_y is the finished calculation of
    # the next position
    x = 0
    while x1+x <= x2:
        y = round(x*slope)
        next_x = x1 + x
        dy = 0
        # stop when we have stacked sufficient vertical coordinates
        while (abs(slope) <= 1 and dy < 1) or \
              (abs(slope) > 1 and dy < math.ceil(abs(slope))):
            if slope < 0: next_y = y1 + y - dy
            else: next_y = y1 + y + dy
            if (slope > 0 and (next_y > y2 or next_x > x2)) or \
               (slope < 0 and (next_y < y2 or next_x > x2)):
                break #Don't overshoot the end
            shape.append((next_x, int(next_y)))
            dy = dy + 1
        x = x+1
    return shape

def polygon(corners, filled=True):
    "A polygon connecting each set of coordinates passed to it via straight lines"
    shape = line(corners[len(corners)-1][0],
                 corners[len(corners)-1][1],
                 corners[0][0],
                 corners[0][1])
    for c in range(len(corners)-1):
        shape.extend(line(corners[c][0],
                          corners[c][1],
                          corners[c+1][0],
                          corners[c+1][1]))
    if filled: return fill_shape(shape)
    else: return shape

def triangle(x1, y1, x2, y2, x3, y3, filled=True):
    corners = ((x1,y1), (x2,y2), (x3,y3))
    return polygon(corners, filled)

def rectangle(x1, y1, x2, y2, x3, y3, x4, y4, filled=True):
    '''
    Draw a shape with four sides (doesn't strictly have to be a rectangle).
    filled: if false, simply returns the outline
    '''
    corners = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
    return polygon(corners, filled)

def circle(center_x, center_y, radius, filled=True, quarters=[1,2,3,4]):
    '''
    Draw a circle, defined by its center point and radius.
    filled: if false, will only draw the outline
    quarters: quarters of the circle to draw (1.TR, 2.BR, 3.BL, 4.TL)
    '''
    shape = []
    for x in range(radius+1):
        for y in range(radius+1):
            distance = round(math.sqrt(x**2+y**2))
            if distance == radius or (filled and distance <= radius):
                if 1 in quarters: shape.append((center_x+x, center_y-y))
                if 2 in quarters: shape.append((center_x+x, center_y+y))
                if 3 in quarters: shape.append((center_x-y, center_y+x))
                if 4 in quarters: shape.append((center_x-y, center_y-x))
    return shape

def fill_shape(shape):
    "Take a shape that only shows the borders and 'colour it out'"
    # Iterate over the shape's enclosing rectangle, adding any points
    # inside the shape to its coordinate list
    filling = []
    xvals = map(lambda c: c[0], shape)
    yvals = map(lambda c: c[1], shape)
    min_x, min_y = min(xvals), min(yvals)
    max_x, max_y = max(xvals), max(yvals)
    # special case where the whole rectangle must be filled
    if ((max_x-min_x) + (max_y-min_y)+2)*2 == len(shape):
        everything = True
    else: everything = False
    for x in range(min_x, max_x+1):
        for y in range(min_y, max_y+1):
            if everything: # this saves a lot of time
                filling.append((x,y))
                continue
            # Every point inside the rectangle has, on the same axis,
            # one shape point larger and one smaller than itself
            # XXX Not perfect, but works for simple (convex) shapes
            surrounding = [False,False,False,False]
            for c in shape:
                if c[0] == x:
                    if c[1] > y: surrounding[0] = True
                    elif c[1] < y: surrounding[1] = True
                elif c[1] == y:
                    if c[0] > x: surrounding[2] = True
                    elif c[0] < x: surrounding[3] = True
                if all(surrounding):
                    filling.append((x,y))
                    break
    shape.extend(filling)
    return shape

