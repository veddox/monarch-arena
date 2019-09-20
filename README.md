# Zoo2 Butterfly Arena Software

## About

This is the software to control the LED arena for the Monarch butterfly experiments
at the Department for Behavioural Physiology and Sociobiology 
([Zoo2](https://www.biozentrum.uni-wuerzburg.de/en/zoo2/research/el-jundi-lab/)), 
University of Würzburg.

The arenas consist of a circular drum with inlaid LED panels
(*8x Adafruit Dotstar 16x16 pixel APA102 RGB LED matrix*). See the `hardware.md`
file for more details.

## Overview

The repository contains a module (`arena.py`) that interfaces with the 
hardware via the [Adafruit DotStar](https://github.com/adafruit/Adafruit_DotStar_Pi)
library and offers a choice between various display modes (`SERIAL`, `PARALLEL`,
`DUPLICATE`, `TEXT`).

The `shape.py` module provides a range of shape drawing functions that can be
used to construct experiment display setups.

There are a couple of scripts to display pre-defined images/animations:

* `house.py` is an example script that draws an image of a house
* `landscape.py` animates two elements moving around a simple landscape
* `dot_bar.py` is a simplified version of the landscape
* `optic_flow.py` simulates optic flow using a moving pattern of vertical bars

These can simply be executed from the commandline.

## Usage

`arena.py` has a rudimentary commandline interface to set either the whole screen
or individual pixels:

```bash
./arena.py clear [colour] #colour defaults to black/off
./arena.py set <x> <y> <colour>
```

To create displays and animations, import the `arena` and `shape` modules. Use 
`arena.set_mode()` to choose a mode. Write a function that does what you want, 
then pass this function to `arena.run()` for safe execution. For more details,
read the API documentation or see the examples in `house.py` and `landscape.py`.

**IMPORTANT:** If you are running this on a Raspberry Pi, delete the `RPi` 
directory and the `dotstar.py` module. These are mockups used during 
development - you will need the real versions installed. (The mockups are already
deleted on the `production` branch, so you can just check that out.) *Weird
things will happen if you forget this!*

---

*&copy; 2018-19 Daniel Vedder, University of Würzburg*  
*Licensed under the terms of the GNU GPLv3.*
