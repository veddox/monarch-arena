
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
import RPi.GPIO as GPIO
from dotstar import Adafruit_DotStar


numpixels = 2048                                 # Number of LEDs in strip

strip = Adafruit_DotStar(numpixels, 2000000)     # declaration of LED strip. 8000000 = 8 MHz SPI CLK rate

red = strip.Color(0, 15, 0);                     # declaration of LED colors
green = strip.Color(1, 0, 0);
blue = strip.Color(0, 0, 1);
off = strip.Color(0, 0, 0);
orange = strip.Color(2,5,0)

magenta =strip.Color(0, 5, 7)
yellow = strip.Color(10, 10, 0)
cyan = strip.Color(10, 0, 10)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)
strip.begin()                                   # Initialize pins for output


#strip.setBrightness(64) # Limit brightness to ~1/4 duty cycle


for i in range (0,numpixels):
	strip.setPixelColor(i, blue);
strip.show()


for j in range (0,2):
	for l in range (6,7)+range(8,9) + range (23,26) + range (2039,2042): 
		strip.setPixelColor(l, orange)
	GPIO.output(33, GPIO.HIGH)
	GPIO.output(37, GPIO.LOW)
	strip.show()
	for p in range(7,8):
		strip.setPixelColor(p, magenta)
	strip.show()
	time.sleep(7)
	for m in range (6,9) + range (23,26) + range (2039,2042):
		strip.setPixelColor(m, blue)
	GPIO.output(33, GPIO.LOW)
	for n in range (1030,1031)+range(1032,1033) + range (1015,1018) + range (1047,1050):
		strip.setPixelColor(n, orange)
	GPIO.output(37, GPIO.HIGH)
	strip.show()
	for q in range (1031,1032):
		strip.setPixelColor(q, magenta)
	strip.show()
	time.sleep(7)
	for o in range (1030,1033) + range (1015,1018) + range (1047,1050):
		strip.setPixelColor(o, blue)
	GPIO.output(37, GPIO.LOW)
	strip.show()

for k in range (0, numpixels):
        strip.setPixelColor(k, off)
	GPIO.output(33, GPIO.LOW)
	GPIO.output(37, GPIO.LOW)
strip.show()
