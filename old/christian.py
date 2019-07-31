#!/usr/bin/python3
### Control the LEDs in the ZooII Monarch butterfly arena.
### Daniel Vedder, April 2018

## --- OBSOLETE --- ##

import sys, math

## ARENA DEFINITIONS

global height, width
height = 16 #default: 16
width = 128 #default: 128

global arena
arena = [False] * height * width

def clear_arena(on=False):
    global arena, height, width
    arena = [on] * height * width
    
def pixel(x, y):
    global height, width
    if x < 0 or y < 0 or x >= width or y >= height:
        raise Exception(str(x)+"/"+str(y)+" is out of bounds.")
    if x%2 == 1:
        return (x+1)*height - y - 1
    else: return x*height + y

## DRAWING FUNCTIONS

def set_pixel(x,y,value=True):
    global arena
    arena[pixel(x,y)] = value

def draw_arena():
    global height, width
    for y in range(height):
        for x in range(width):
            if arena[pixel(x,y)]: sys.stdout.write('X')
            else: sys.stdout.write('-')
        sys.stdout.write('\n')
        sys.stdout.flush()

def draw_shape(coords, on=True, flush=True):
    for c in coords:
        set_pixel(c[0], c[1], on)
    if flush: draw_arena()

## SHAPE DEFINITIONS
## A shape is a list of coordinate tuples whose pixels are to be drawn
        
def line(x1, y1, x2, y2):
    if x1 == x2:
        return vertical_line(x1, y1, y2)
    elif y1 == y2:
        return horizontal_line(y1, x1, x2)
    else: return diagonal_line(x1, y1, x2, y2)

def horizontal_line(y, x1, x2):
    shape = []
    if x2 < x1: x1,x2 = x2,x1
    for x in range(x1, x2+1):
        shape = shape + [(x, y)]
    return shape

def vertical_line(x, y1, y2):
    shape = []
    if y2 < y1: y1,y2 = y2,y1
    for y in range(y1, y2+1):
        shape = shape + [(x, y)]
    return shape

def diagonal_line(x1, y1, x2, y2):
    if x2 < x1:
        x1,x2 = x2, x1
        y1,y2 = y2, y1
    shape = []
    slope = (x2-x1)/(y2-y1)
    # XXX a bit ugly, but it works
    if abs(slope) < 1: # steep lines
        for y in range(y1, y2+1):
            x = round(x2 - ((y2-y)*slope))
            shape = shape + [(x,y)]
    else: # shallow lines
        for x in range(x1, x2+1):
            y = round(y2 - ((x2-x)/slope))
            shape = shape + [(x,y)]
    return shape

def polygon(corners):
    shape = line(corners[len(corners)-1][0], corners[len(corners)-1][1],
                  corners[0][0], corners[0][1])
    for c in range(len(corners)-1):
        shape = shape + line(corners[c][0], corners[c][1],
                             corners[c+1][0], corners[c+1][1])
    return shape

def triangle(x1, y1, x2, y2, x3, y3):
    corners = ((x1,y1), (x2,y2), (x3,y3))
    return polygon(corners)

def rectangle(x1, y1, x2, y2, x3, y3, x4, y4):
    corners = ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
    return polygon(corners)

def circle(center_x, center_y, radius, show_center=False):
    if show_center: shape = [(center_x, center_y)]
    else: shape = []
    for x in range(radius):
        y = round(math.sqrt(radius**2-x**2))
        shape = shape + [(center_x+x, center_y+y), (center_x+x, center_y-y),
                         (center_x-x, center_y+y), (center_x-x, center_y-y),
                         (center_x+y, center_y+x), (center_x+y, center_y-x),
                         (center_x-y, center_y+x), (center_x-y, center_y-x)]
    return shape


## COMPLEX IMAGES

def draw_house():
    # Just playing around ;-)
    draw_shape(line(0,15,127,15), flush=False) #grass
    draw_shape(rectangle(24,15,72,15,72,7,24,7), flush=False) #main house
    draw_shape(rectangle(20,7,24,3,72,3,76,7), flush=False) #roof
    draw_shape(rectangle(58,15,58,10,64,10,64,15), flush=False) #door
    draw_shape(rectangle(32,9,44,9,44,12,32,12), flush=False) #window
    draw_shape(circle(99,6,5), flush=False) #tree foliage
    draw_shape(rectangle(98,11,100,11,100,15,98,15)) #tree trunk
