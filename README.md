# Zoo2 Butterfly Arena Software

## About

This is the software to control the LED arena for the Monarch butterfly experiments
at the Department for Behavioural Physiology and Sociobiology 
([Zoo2](https://www.biozentrum.uni-wuerzburg.de/en/zoo2/research/el-jundi-lab/)), 
University of Würzburg.

The arenas consist of a circular drum with inlaid LED panels
(*8x Adafruit Dotstar 16x16 pixel APA102 RGB LED matrix*).

## Overview

The repository contains a module (`arena.py`) that interfaces with the 
hardware via the [Adafruit DotStar](https://github.com/adafruit/Adafruit_DotStar_Pi)
library and offers a choice between various display modes (`SERIAL`, `PARALLEL`,
`DUPLICATE`, `TEXT`).

The `draw.py` module provides a range of shape drawing functions that can be
used to construct experiment display setups.

There are a couple of scripts to display pre-defined images/animations:

* `house.py` is an example script that draws an image of a house
* *work in progress...*

## Usage

`arena.py` has a rudimentary commandline interface to set either the whole screen
or individual pixels:

```bash
./arena.py clear [colour] #colour defaults to black/off
./arena.py set <x> <y> <colour>
```

<!--obsolete-->
(Use `--serial` or `--parallel` before the clear/set command to choose a mode.)

**NOTE:** If you're running this on a Raspberry Pi, delete the `RPi` directory
and the `dotstar.py` module. These are mockups used during development - you will
need the real versions installed!

---

*&copy; 2018-19 Daniel Vedder, University of Würzburg*  
*Licensed under the terms of the MIT License.*
