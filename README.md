# Zoo2 Butterfly Arena Software

## About

This is the software to control the LED arena for the Monarch butterfly experiments
at the Department for Behavioural Physiology and Sociobiology 
([Zoo2](https://www.biozentrum.uni-wuerzburg.de/en/zoo2/research/el-jundi-lab/)), 
University of Würzburg.

The arenas consist of a circular drum with inlaid LED panels. <!--TODO make/model?-->

## Overview

This repository contains a small library (`arena.py`) that interfaces with the 
hardware (via the [Adafruit DotStar](https://github.com/adafruit/Adafruit_DotStar_Pi)
library) and offers basic graphic functions.

It also contains a range of scripts to display pre-defined images/animations.

## Usage

`arena.py` has a rudimentary commandline interface to set either the whole screen
or individual pixels:

```bash
./arena.py clear [colour] #colour defaults to black/off
./arena.py set <x> <y> <colour>
```

(Use `--serial` or `--parallel` before the clear/set command to choose a mode.)

`house.py` is an example script that draws an image of a house.

---

*&copy; 2018-19 Daniel Vedder, University of Würzburg*  
*Licensed under the terms of the MIT License.*
