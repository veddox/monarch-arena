
#!/usr/bin/python
#This is Ofstad3 written by Keram Pfeiffer on January 26th, 2018
#The program addresses a 16x128 pixel rgb LED APA102 Matrix and creates a pattern similar to that used in Ofstad et al. 2011

# ToDo:
# address bg LEds for oblique stripes rather than entire bg and then paint fg over it
# fix loop such that there is no accumulation of offset
# put each stripe pattern into functions to make calls more flexible
# vary width by using variables for stripe widths=?
# stripes in Ofstad are tilted other way

import time
import random
from dotstar import Adafruit_DotStar

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#select parallel or serial mode
GPIO.setup(25, GPIO.OUT)
GPIO.output(25,GPIO.HIGH)   #seriell
#GPIO.output(25,GPIO.LOW)     #parallel

#GPIOs for stimedent and stimstart/end
GPIO.setup(26, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.output(26,GPIO.LOW)
GPIO.output(19,GPIO.LOW)


numpixels = 2048                                 # Number of LEDs in strip

strip = Adafruit_DotStar(numpixels, 10000000)     # declaration of LED strip. 8000000 = 8 MHz SPI CLK rate

red = strip.Color(0, 15, 0);                     # declaration of LED colors
green = strip.Color(15, 0, 0);
blue = strip.Color(0, 0, 10);
off = strip.Color(0, 0, 0);

magenta =strip.Color(0, 10, 10)
yellow = strip.Color(10, 10, 0)
cyan = strip.Color(10, 0, 10)

fgcolor = green                                 # foreground color of pattern
bgcolor = red                                # background color of pattern

glob_offs = 0                                   # global offset (used to shift the entire pattern
hbars_offs = 0                              # offset of horizontal bars
vbars_offs = 0                 # offset of vertical bars
oblbars_offs = 0                                # offset of oblique bars

waittime = 0.015
strip.begin()                                   # Initialize pins for output


#strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle
n=0
numrot = 5
while n< numrot:
	for i in range (0,1):
		time.sleep(0.01)
		GPIO.output(19, GPIO.HIGH)
		GPIO.output(19, GPIO.LOW)
	GPIO.output(26, GPIO.HIGH)
	GPIO.output(26, GPIO.LOW)


	newpos=0;
  
    
	for i in range (0,numpixels):
		strip.setPixelColor(i, off);
	strip.show()
	
       
    
	for j in range (0, 128):
#		for i in range ((j-1)*16, (j-1)*16+16):
#			strip.setPixelColor(i,off);
#
		for i in range (j*16, j*16+16):
			strip.setPixelColor(i, green);
            	strip.show()
            	time.sleep(waittime)            
		for i in range (j*16, j*16+16):
			strip.setPixelColor(i, off);
		
#		for i in range ((j-1)*16, (j-1)*16+ 16):
#        		strip.setPixelColor(i, off);
 #          strip.show()
 #       	time.sleep(waittime)

	strip.show();
	GPIO.output(26, GPIO.HIGH)
	GPIO.output(26, GPIO.LOW)
	n+=1;
	
