# Application Programmer Interface

*This is an overview of functions and variables that can be used when writing new
animation scripts for the monarch arena. For a complete understanding of how
the library works, read the source.*

## arena.py

- `MODE` A string value indicating the output mode for the arena. Possible
  values: "SERIAL" (legacy mode), "PARALLEL" (default), "DUPLICATE" (all arena
  panels show the same image), "TEXT" (output as ASCII to computer screen).
  **IMPORTANT:** Do *not* change this directly. Use `set_mode()` or `run()`
  instead.
  
- `colours` A dict mapping colour names to their RGB values (for arena output) 
  or a letter (for ASCII output).
  
- `arena` An internal representation of the screen, implemented as a list of
  colour strings. **Do not modify.**

- `set_mode(new_mode)` Change the output mode and do all associated
  housekeeping.
  
- `toggle_panel(panel, value=None)` Turn a single panel (0-7) on or off. 
  (value == True -> on, value == False -> off, value == None -> toggle). 
  *Can only be used in DUPLICATE mode!*

- `clear(colour="black", show=True)` Clear the screen (i.e. set it all to one
  colour). If `show` is true, render immediately.
  
- `pixel(x,y)` Get the current colour of this pixel.

- `set_pixel(x,y,colour)` Set a pixel to a given colour. (**Note:** does not
  output to screen, call `render()` for that.)
  
- `render()` Output the current state of `arena` to the device.

- `run(display_fn, mode=None)` Safely execute a function object, making sure to
  clean up afterwards and catching any errors or keyboard interrupts (by Ctrl-C).
  Can optionally be used to set the output mode. **This is the main entry point
  and should be the final function called by a script.**
  
## shape.py

- `plot(coords, colour="green", flush=False)` Draw a shape in a given colour, 
  using a list of coordinates such as supplied by the following shape functions.
  Renders immediately if `flush` is true.
  
*Note: All following functions return a list of coordinates that may be passed
to `plot()`.*
  
- `line(x1, y1, x2, y2)` Approximate a straight line between two points.

- `polygon(corners, filled=True)` Construct a shape by linking the corners,
  optionally filling it out. `corners`: a list of pairs of coordinates.
  
- `triangle(x1, y1, x2, y2, x3, y3, filled=True)` Returns a triangle.

- `rectangle(x1, y1, x2, y2, x3, y3, x4, y4, filled=True)` Returns a rectangle.

- `circle(center_x, center_y, radius, filled=True, quarters=[1,2,3,4])`
  Create a circle using its center point and radius, optionally specifying which
  quadrants to draw.

- `fill_shape(shape)` Take a shape (a list of coordinates enclosing a space)
  and append all coordinates inside its boundaries.
