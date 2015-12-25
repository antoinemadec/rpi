#!/usr/bin/python
# Example using a character LCD plate.
import math
import time

import Adafruit_CharLCD as LCD

def banner(s, period=0.5):
    s_long = s + " "
    while True:
        lcd.home()
        lcd.message(s_long)
        s_long = s_long[1:]+s_long[0]
        time.sleep(period)

# Initialize the LCD using the pins 
lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()
lcd.set_color(1,1,1)

lcd.clear()
lcd.message ("Nathalie")
time.sleep(1)
lcd.clear()

banner("J'aime la verif !!!!")


# Make list of button value, text, and backlight color.
#		if lcd.is_pressed(button[0]):
#buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
#            (LCD.LEFT,   'Left'  , (1,0,0)),
#            (LCD.UP,     'Up'    , (0,0,1)),
#            (LCD.DOWN,   'Down'  , (0,1,0)),
#            (LCD.RIGHT,  'Right' , (1,0,1)) )
