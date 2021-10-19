#!/usr/bin/env python

import datetime
import board
import neopixel
from config import config_ag as config
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
    elif 5 <= minute < 10:
        return config.FIMF + config.AB
    elif 10 <= minute < 15:
        return config.ZAE + config.AB
    elif 15 <= minute < 20:
        return config.VIERTEL + config.AB
    elif 20 <= minute < 25:
        return config.ZWANZIG + config.AB
    elif 25 <= minute < 30:
        return config.FIMF + config.VOR + config.HALBI
    elif 30 <= minute < 35:
        return config.HALBI
    elif 35 <= minute < 40:
        return config.FIMF + config.AB + config.HALBI
    elif 40 <= minute < 45:
        return config.ZWANZIG + config.VOR
    elif 45 <= minute < 50:
        return config.VIERTEL + config.VOR
    elif 50 <= minute < 55:
        return config.ZAE + config.VOR
    elif minute >= 55:
        return config.FIMF + config.VOR
    return []

def getHour(hour, minute):
    print(hour)
    if hour >= 12:
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
        response = requests.get("http://" + config.PI_HOSTNAME + "/color")
        if (response.status_code != 200):
            print("Error!", response.status_code)
            return config.DEFAULT_COLOR
        response = response.json()
        return (response[0], response[1], response[2])
    except requests.ConnectionError as error:
        print(error)
        return config.DEFAULT_COLOR

def getBrightness():
    try:
        response = requests.get("http://" + config.PI_HOSTNAME + "/brightness")
        if (response.status_code != 200):
            print("Error!", response.status_code)
            return config.DEFAULT_BRIGHTNESS
        response = response.json()
        return response
    except requests.ConnectionError as error:
        print(error)
        return config.DEFAULT_BRIGHTNESS

def changeNeeded():
    global lastMinute
    global color
    if minute != lastMinute:
        lastMinute = minute
        print("time change detected")
        return True
    return False

def isNightmode(hour):
    return hour >= config.NIGHTMODE_START or hour < config.NIGHTMODE_END

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
    pixel_pin, num_pixels, brightness=config.DEFAULT_BRIGHTNESS, auto_write=False, pixel_order=order
)

print("start")
resetLED()

lastMinute = None
color = config.DEFAULT_COLOR
brightness = config.DEFAULT_BRIGHTNESS

while True:
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if changeNeeded():
        # resetLED()

        brightness = getBrightness()

        if isNightmode(hour):
            brightness = config.NIGHTMODE_BRIGHTNESS

        color = getColor()
        timeArray = getTime(hour, minute)
        pixels.brightness = brightness
        print("time: ", timeArray)
        print("color: ", color)
        print("brightness: ", brightness)

        show(timeArray, color)
