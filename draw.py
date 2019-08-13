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

import math, time, random ##XXX the latter two are not yet needed
import arena

def shape(coords, colour="green", flush=False):
    '''
    Draw a shape from a list of coordinates (as produced by the shape functions).
    colour: The colour to use
    flush: If true, will output the result immediately
    '''
    for c in coords:
        arena.set_pixel(c[0], c[1], colour)
    if flush: arena.draw_arena()

## SHAPE DEFINITIONS
## A shape is a list of coordinate tuples whose pixels are to be drawn
        
def line(x1, y1, x2, y2):
    "A straight line from x1/y1 to x2/y2"
    if x1 == x2:
        return vertical_line(x1, y1, y2)
    elif y1 == y2:
        return horizontal_line(y1, x1, x2)
    else: return diagonal_line(x1, y1, x2, y2)

def horizontal_line(y, x1, x2):
    shape = []
    if x2 < x1: x1,x2 = x2,x1
    for x in range(x1, x2+1):
        shape.append((x, y))
    return shape

def vertical_line(x, y1, y2):
    shape = []
    if y2 < y1: y1,y2 = y2,y1
    for y in range(y1, y2+1):
        shape.append((x, y))
    return shape

def diagonal_line(x1, y1, x2, y2):
    #FIXME is this broken? cf. `landscape.py`
    if x2 < x1:
        x1,x2 = x2, x1
        y1,y2 = y2, y1
    shape = []
    slope = (x2-x1)/(y2-y1)
    # XXX a bit ugly, but it works
    if abs(slope) < 1: # steep lines
        for y in range(y1, y2+1):
            x = int(round(x2 - ((y2-y)*slope)))
            shape.append((x,y))
    else: # shallow lines
        for x in range(x1, x2+1):
            y = int(round(y2 - ((x2-x)/slope)))
            shape.append((x,y))
    return shape

def polygon(corners):
    "A polygon connecting each set of coordinates passed to it via straight lines"
    #TODO add `filled` option (see Lisp library)
    shape = line(corners[len(corners)-1][0],
                 corners[len(corners)-1][1],
                 corners[0][0],
                 corners[0][1])
    for c in range(len(corners)-1):
        shape.extend(line(corners[c][0],
                          corners[c][1],
                          corners[c+1][0],
                          corners[c+1][1]))
    return shape

def triangle(x1, y1, x2, y2, x3, y3):
    corners = ((x1,y1), (x2,y2), (x3,y3))
    return polygon(corners)

def rectangle(x1, y1, x2, y2, x3, y3, x4, y4, filled=False):
    '''
    Draw a shape with four sides (doesn't strictly have to be a rectangle).
    filled: if false, simply returns the outline
    '''
    corners = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
    outline = polygon(corners)
    if not filled: return outline
    shape = outline
    for x in range(min(x1,x2,x3,x4), max(x1,x2,x3,x4)+1):
        for y in range(min(y1,y2,y3,y4), max(y1,y2,y3,y4)+1):
            conds = []
            for c in outline:
                # Every point inside the rectangle has, on the same
                # axis, one point larger and one smaller than itself
                if x == c[0] and y < c[1]: conds.append("yl")
                elif x == c[0] and y > c[1]: conds.append("yg")
                if y == c[1] and x < c[0]: conds.append("xl")
                elif y == c[1] and x > c[0]: conds.append("xg")
            if "yl" in conds and "yg" in conds and "xl" in conds and "xg" in conds:
                shape.append((x,y))
    return shape

def circle(center_x, center_y, radius, filled=False, quarters=[1,2,3,4]):
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

## ANIMATION FUNCTIONS
# TODO
