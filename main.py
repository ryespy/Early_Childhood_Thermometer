# Early Childhood Thermometer
# Ryan Cain
# 30 NOV 2017
# Thanks to the Adafruit Learning System and the Adafruit Dicord Community
# Especially @tannewt @kattni @cater

from digitalio import *
from board import *
import time
import neopixel
import busio
import adafruit_mcp9808
import adafruit_ds3231

#################helpers###############################################
NUMPIXELS = 12
NP = neopixel.NeoPixel(D5, NUMPIXELS, brightness=.5, auto_write=False)

pixels = neopixel.NeoPixel(NEOPIXEL, 1)
pixels[0] = (0,0,0)
pixels.show()

led = DigitalInOut(D13)  # Button LED
led.direction = Direction.OUTPUT

button = DigitalInOut(D11)
button.direction = Direction.INPUT
button.pull = Pull.UP

tdelay= 5
tstatus = 0

blu= (0,0,255)
cyn= (0,255,255)
grn= (0,255,0)
yel= (255,255,0)
red= (255,0,0)
mag= (255,0,255)
ooff= (0,0,0)

def fahrenheit(celsius):
  return (celsius * 9 / 5) + 32

def set_thermometer_pixels(n, color):
    NP.fill(0)
    NP[0:n] = (color,)*n
    NP.show()

######################### MAIN LOOP ##############################

while True:
  with busio.I2C(SCL, SDA) as i2c: #read the current datetime
      rtc = adafruit_ds3231.DS3231(i2c)
        #print (rtc.datetime)
      dt= rtc.datetime

  with busio.I2C(SCL, SDA) as i2c: #read the current temperature
      t = adafruit_mcp9808.MCP9808(i2c)
      tempf= fahrenheit(t.temperature)
      tempc= t.temperature
  print (dt.tm_year, "-", dt.tm_mon,"-", dt.tm_mday, " ", dt.tm_hour, ":", dt.tm_min, ":", dt.tm_sec, "," , tempf, "," ,tempc, sep='')


  if button.value: #NO Button press do nothing, unless time ==12:00
    print('not')
    led.value = False      # turn OFF LED
    set_thermometer_pixels(12, ooff)  # turn OFF neopixels

  else:
    print('pressed')
    led.value = True       # turn ON LED

    try:
        with open("/temperature.txt", "a") as fp:
          #while True:
            fp.write('{}-{}-{} {:02}:{:02}:{:02}, {},{}\n'.format(dt.tm_year, dt.tm_mon, dt.tm_mday, dt.tm_hour, dt.tm_min, dt.tm_sec, tempf, tempc))
            fp.flush()
            led.value = not led.value
            time.sleep(.2)
    except OSError as e:
        delay = 0.5
        if e.args[0] == 28:
            delay = 0.25
        while True:
            led.value = not led.value
            time.sleep(delay)
    else:
      if tempf > 105:
       set_thermometer_pixels (12, mag)
      elif tempf > 95:
       set_thermometer_pixels (11, mag)
      elif tempf > 85:
       set_thermometer_pixels (10, red)
      elif tempf > 75:
       set_thermometer_pixels (9, red)
      elif tempf > 65:
       set_thermometer_pixels (8, yel)
      elif tempf > 55:
       set_thermometer_pixels (7, yel)
      elif tempf > 45:
       set_thermometer_pixels (6, grn)
      elif tempf > 35:
       set_thermometer_pixels (5, grn)
      elif tempf > 25:
       set_thermometer_pixels (4, cyn)
      elif tempf > 15:
       set_thermometer_pixels (3, cyn)
      elif tempf > 5:
       set_thermometer_pixels (2, blu)
      else:
       NP[0]=blu
       NP.show()
    time.sleep(tdelay)
