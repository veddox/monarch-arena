#!/usr/bin/python2
### Gives an example of how to use arena.py
### Draws a house with a tree :-)
###
### Daniel Vedder, April 2018


##TODO Check if this still works

import arena
import draw

arena.MODE = "TEXT"

arena.clear_arena("blue") #sky #XXX Change to "blue" for use in the actual arena

# Note the order of drawing! (Some shapes overlap)
draw.shape(draw.rectangle(24,15,72,15,72,7,24,7,True), colour="orange", flush=False) #main house
draw.shape(draw.rectangle(20,7,24,3,72,3,76,7,True), colour="red", flush=False) #roof
draw.shape(draw.rectangle(58,15,58,10,64,10,64,15,True), colour="magenta", flush=False) #door
arena.set_pixel(63,12,"red") #doorknob
draw.shape(draw.rectangle(32,9,44,9,44,12,32,12,True), colour="cyan", flush=False) #window
draw.shape(draw.rectangle(98,11,100,11,100,15,98,15,True), colour="magenta", flush=False) #tree trunk
draw.shape(draw.circle(99,6,5,True), colour="green", flush=False) #tree foliage
draw.shape(draw.circle(122,3,2,True), colour="yellow", flush=False) #sun

draw.shape(draw.line(0,15,127,15), colour="green") #grass

# Note: the drawn image is not deleted in this script.
# To clear the arena screen again, call the following from the commandline:
# './arena.py clear'
