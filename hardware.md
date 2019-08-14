# Arena hardware description

The purpose of the Zoo2 butterfly arenas is to study visual navigation in 
monarch butterflies (*Danaus plexippus*).

## Setup and components

The arenas are manufactured by the Biocenter's in-house workshop. They consist 
of an open-ended drum (ca. 30cm high, 60cm diameter), clad on the inside with 
eight LED panels (Adafruit Dotstar 16x16 pixel APA102 RGB LED matrices).

The insect to be studied can be suspended from the top center of the drum in 
such a way that it can turn as it "flies", but not actually change its 
position. It can then be shown various patterns and animations, as its 
response to these is observed.

## Wiring

Each arena is controlled by a Raspberry Pi via its GPIO pins. Pins `10` and `11`
are used by the Adafruit Dotstar control library for data output and clock 
timing, respectively. (The library holds an internal pixel buffer whose contents
are pushed to all active panels when its `show()` method is called.) 

Pin `25` switches over between serial mode (all panels are treated as one large,
combined panel - legacy mode) or parallel mode (panels can be addressed
individually - better performance).

Pins `5,6,13,19,26,16,20,21` activate or deactivate the panels.
