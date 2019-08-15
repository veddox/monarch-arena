#!/usr/bin/python2
### Gives an example of how to use arena.py
### Draws a house with a tree :-)
###
### Daniel Vedder, April 2018
### Licensed under the terms of the GNU GPLv3

import arena
import draw

arena.set_mode("PARALLEL")
arena.clear_arena("blue", show=False) #sky

# Note the order of drawing! (Some shapes overlap)
draw.shape(draw.rectangle(24,15,72,15,72,7,24,7,True), colour="orange") #main house
draw.shape(draw.rectangle(20,7,24,3,72,3,76,7,True), colour="red") #roof
draw.shape(draw.rectangle(58,15,58,10,64,10,64,15,True), colour="magenta") #door
arena.set_pixel(63,12,"red") #doorknob
draw.shape(draw.rectangle(32,9,44,9,44,12,32,12,True), colour="cyan") #window
draw.shape(draw.rectangle(98,11,100,11,100,15,98,15,True), colour="magenta") #tree trunk
draw.shape(draw.circle(99,6,5,True), colour="green") #tree foliage
draw.shape(draw.circle(122,3,2,True), colour="yellow") #sun
draw.shape(draw.line(0,15,127,15), colour="green") #grass

arena.draw_arena()

# Note: the drawn image is not deleted in this script.
# To clear the arena screen again, call the following from the commandline:
# './arena.py clear'
