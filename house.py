#!/usr/bin/python2
### Gives an example of how to use arena.py
### Draws a house with a tree :-)
###
### Daniel Vedder, April 2018

from arena import * #Not good style to import everything, but it saves typing

clear_arena("blue") #sky #XXX Change to "blue" for use in the actual arena

# Note the order of drawing! (Some shapes overlap)
draw_shape(rectangle(24,15,72,15,72,7,24,7,True), colour="orange", flush=False) #main house
draw_shape(rectangle(20,7,24,3,72,3,76,7,True), colour="red", flush=False) #roof
draw_shape(rectangle(58,15,58,10,64,10,64,15,True), colour="magenta", flush=False) #door
set_pixel(63,12,"red") #doorknob
draw_shape(rectangle(32,9,44,9,44,12,32,12,True), colour="cyan", flush=False) #window
draw_shape(rectangle(98,11,100,11,100,15,98,15,True), colour="magenta", flush=False) #tree trunk
draw_shape(circle(99,6,5,True), colour="green", flush=False) #tree foliage
draw_shape(circle(122,3,2,True), colour="yellow", flush=False) #sun

draw_shape(line(0,15,127,15), colour="green",draw=False) #grass
#XXX In the previous line, remove draw=False for use in the actual arena

# Note: the drawn image is not deleted in this script.
# To clear the arena screen again, call the following from the commandline:
# './arena.py clear'
