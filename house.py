#!/usr/bin/python2
### Gives an example of how to use arena.py
### Draws a house with a tree :-)
###
### Daniel Vedder, April 2018
### Licensed under the terms of the GNU GPLv3

import arena
import shape

def draw_house():
    arena.clear("black", show=False) #sky #XXX Change to "blue" for use in the actual arena
    # Note the order of drawing! (Some shapes overlap)
    shape.plot(shape.rectangle(24,15,72,15,72,7,24,7), colour="orange") #main house
    shape.plot(shape.rectangle(20,7,24,3,72,3,76,7), colour="red") #roof
    shape.plot(shape.rectangle(58,15,58,10,64,10,64,15), colour="magenta") #door
    arena.set_pixel(63,12,"red") #doorknob
    shape.plot(shape.rectangle(32,9,44,9,44,12,32,12), colour="cyan") #window
    shape.plot(shape.rectangle(98,11,100,11,100,15,98,15), colour="magenta") #tree trunk
    shape.plot(shape.circle(99,6,5), colour="green") #tree foliage
    shape.plot(shape.circle(122,3,2), colour="yellow") #sun
    shape.plot(shape.line(0,15,127,15), colour="green") #grass
    arena.render()

arena.run(draw_house, "TEXT") #TODO change to "PARALLEL" or "SERIAL"
    
# Note: the drawn image is not deleted in this script.
# To clear the arena screen again, call the following from the commandline:
# './arena.py clear'
