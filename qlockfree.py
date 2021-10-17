#!/usr/bin/env python

import time
import datetime
import board
import neopixel
import requests
import configparser

parser = configparser.ConfigParser()
parser.read('config.ini')
config = parser['aargau']

def resetLED():
    for i in range(num_pixels):
        pixels[i] = config.get('colorBlank')
        pixels.show()

def getTime(hour, minute):
    time = []

    time = time + config.get('es') + config.get('isch') + getMinute(minute) + getSingleMinute(minute) + getHour(hour, minute)

    return time

def getSingleMinute(minute):
    singleMinute = minute % 5

    if singleMinute == 0:
        return []
    elif singleMinute == 1:
        return config.get('plus_one')
    elif singleMinute == 2:
        return config.get('plus_two') + config.get('plus_one')
    elif singleMinute == 3:
        return config.get('plus_three') + config.get('plus_two') + config.get('plus_one')
    elif singleMinute == 4:
        return config.get('plus_four') + config.get('plus_three') + config.get('plus_two') + config.get('plus_one')
    return []

def getMinute(minute):
    if minute == 0:
        return []
    elif 5 <= minute < 10:
        return config.get('fimf') + config.get('ab')
    elif 10 <= minute < 15:
        return config.get('zae') + config.get('ab')
    elif 15 <= minute < 20:
        return config.get('viertel') + config.get('ab')
    elif 20 <= minute < 25:
        return config.get('zwanzig') + config.get('ab')
    elif 25 <= minute < 30:
        return config.get('fimf') + config.get('vor') + config.get('halbi')
    elif 30 <= minute < 35:
        return config.get('halbi')
    elif 35 <= minute < 40:
        return config.get('fimf') + config.get('ab') + config.get('halbi')
    elif 40 <= minute < 45:
        return config.get('zwanzig') + config.get('vor')
    elif 45 <= minute < 50:
        return config.get('viertel') + config.get('vor')
    elif 50 <= minute < 55:
        return config.get('zae') + config.get('vor')
    elif minute >= 55:
        return config.get('fimf') + config.get('vor')
    return []

def getHour(hour, minute):
    print(hour)
    if hour >= 12:
        hour = hour - 12
    if minute >= 25:
        hour = hour + 1
    if hour == 0:
        return config.get('zwelfi')
    elif hour == 1:
        return config.get('ains')
    elif hour == 2:
        return config.get('zwai')
    elif hour == 3:
        return config.get('drey')
    elif hour == 4:
        return config.get('vieri')
    elif hour == 5:
        return config.get('fimfi')
    elif hour == 6:
        return config.get('saggsi')
    elif hour == 7:
        return config.get('siibeni')
    elif hour == 8:
        return config.get('achti')
    elif hour == 9:
        return config.get('nyyni')
    elif hour == 10:
        return config.get('zaani')
    elif hour == 11:
        return config.get('elfi')
    elif hour == 12:
        return config.get('zwelfi')
    return []

def getColor():
    try:
        response = requests.get("http://raspberrypi/color")
        if (response.status_code != 200):
            print("Error!", response.status_code)
            return config.get('color')
        response = response.json()
        return (response[0], response[1], response[2])
    except requests.ConnectionError as error:
        print(error)
        return config.get('color')

def changeNeeded():
    global lastMinute
    global color
    if minute != lastMinute:
        lastMinute = minute
        print("time change detected")
        return True
    return False

def isNightmode(hour):
    return hour >= config.get('nightmode_start') or hour < config.get('nightmode_end')

def show(timeArray, color):
    for i in range(num_pixels):
        if i in timeArray:
            pixels[i] = color
        else:
            pixels[i] = config.get('colorBlank')
    pixels.show()

def test():
    for i in range(num_pixels):
        pixels[i] = config.get('color')
    pixels.show()

pixel_pin = board.D18
num_pixels = 114
order = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=config.get('brightness'), auto_write=False, pixel_order=order
)

print("start")
resetLED()

lastMinute = None
color = config.get('color')

while True:
    now = datetime.datetime.now()
    hour = now.hour
    minute = now.minute

    if changeNeeded():
        # resetLED()
        if isNightmode(hour):
            pixels.brightness = config.get('nightmode_brightness')
        else:
            pixels.brightness = config.get('brightness')

        color = getColor()
        timeArray = getTime(hour, minute)
        print("time: ", timeArray)
        print("color: ", color)
        print("brightness: ", pixels.brightness)

        show(timeArray, color)
