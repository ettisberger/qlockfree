#!/usr/bin/env python

import time 
import datetime
import board
import neopixel
import config
import requests

def resetLED():
    for i in range(num_pixels):
        pixels[i] = config.COLOR_NONE
        pixels.show()

def getTime(hour, minute):
    time = []

    time = time + config.ES + config.ISCH + getMinute(minute) + getSingleMinute(minute) + getHour(hour, minute)

    return time

def getSingleMinute(minute):
    singleMinute = minute % 5

    if singleMinute == 0:
        return []
    elif singleMinute == 1:
        return config.PLUS_ONE 
    elif singleMinute == 2:
        return config.PLUS_TWO + config.PLUS_ONE
    elif singleMinute == 3:
        return config.PLUS_THREE + config.PLUS_TWO + config.PLUS_ONE
    elif singleMinute == 4:
        return config.PLUS_FOUR + config.PLUS_THREE + config.PLUS_TWO + config.PLUS_ONE
    return []

def getMinute(minute):
    if minute == 0:
        return []
    elif minute >= 5 and minute < 10:
        return config.FIMF + config.AB
    elif minute >= 10 and minute < 15:
        return config.ZAE + config.AB
    elif minute >= 15 and minute < 20:
        return config.VIERTEL + config.AB
    elif minute >= 20 and minute < 25:
        return config.ZWANZIG + config.AB
    elif minute >= 25 and minute < 30:
        return config.FIMF + config.VOR + config.HALBI
    elif minute >= 30 and minute < 35:
        return config.HALBI
    elif minute >= 35 and minute < 40:
        return config.FIMF + config.AB + config.HALBI
    elif minute >= 40 and minute < 45:
        return config.ZWANZIG + config.VOR
    elif minute >= 45 and minute < 50:
        return config.VIERTEL + config.VOR
    elif minute >= 50 and minute < 55:
        return config.ZAE + config.VOR
    elif minute >= 55:
        return config.FIMF + config.VOR
    return []

def getHour(hour, minute):
    if hour > 12:
        hour = hour - 12
    if minute >= 25:
        hour = hour + 1 
    if hour == 0:
        return config.ZWELFI
    elif hour == 1:
        return config.AINS
    elif hour == 2:
        return config.ZWAI
    elif hour == 3:
        return config.DREY
    elif hour == 4:
        return config.VIERI
    elif hour == 5:
        return config.FIMFI
    elif hour == 6:
        return config.SAGGSI
    elif hour == 7:
        return config.SIIBENI
    elif hour == 8:
        return config.ACHTI
    elif hour == 9:
        return config.NYYNI
    elif hour == 10:
        return config.ZAANI
    elif hour == 11:
        return config.ELFI
    elif hour == 12:
        return config.ZWELFI
    return []

def getColor():
    try:
        response = requests.get("http://raspberrypi/color")
        if (response.status_code != 200):
            print("Error!", response.status_code)
            return config.DEFAULT_COLOR
        response = response.json()
        return (response[0], response[1], response[2])
    except requests.ConnectionError as error:
        print(error)
        return config.DEFAULT_COLOR

def changeNeeded():
    global lastMinute
    global color 
    if minute != lastMinute:
        lastMinute = minute
        print("time change detected")
        return True
    return False

def show(timeArray, color):
    for i in range(num_pixels):
        if i in timeArray:
            pixels[i] = color
        else:
            pixels[i] = config.COLOR_NONE
    pixels.show()

def test():
    for i in range(num_pixels):
        pixels[i] = config.DEFAULT_COLOR
    pixels.show()

pixel_pin = board.D18
num_pixels = 114
order = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.8, auto_write=False, pixel_order=order
)

print("start")
resetLED()

lastMinute = None
color = config.DEFAULT_COLOR 

while True:
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if changeNeeded():
        # resetLED()
        color = getColor()
        timeArray = getTime(hour, minute)
        print("time: ", timeArray)
        print("color: ", color)
        show(timeArray, color)
