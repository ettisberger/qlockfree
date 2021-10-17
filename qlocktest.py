#!/usr/bin/env python

import time 
import datetime
import board
import neopixel
from config import config_ag as config

def resetLED():
    for i in range(num_pixels):
        pixels[i] = config.COLOR_NONE
        pixels.show()

def show(timeArray, color):
    for i in range(num_pixels):
        if i in timeArray:
            pixels[i] = color
        else:
            pixels[i] = config.COLOR_NONE
    pixels.show()

def test():
    testArrays = [] * 20

    testArrays.append(config.ES + config.ISCH)
    testArrays.append(config.ES + config.ISCH + config.FIMF)
    testArrays.append(config.ES + config.ISCH + config.ZAE)
    testArrays.append(config.ES + config.ISCH + config.ZWANZIG)
    testArrays.append(config.ES + config.ISCH + config.FIMF + config.AB)
    testArrays.append(config.ES + config.ISCH + config.ZAE + config.AB)
    testArrays.append(config.ES + config.ISCH + config.ZWANZIG + config.AB)
    testArrays.append(config.ES + config.ISCH + config.FIMF + config.VOR)
    testArrays.append(config.ES + config.ISCH + config.ZAE + config.VOR)
    testArrays.append(config.ES + config.ISCH + config.ZWANZIG + config.VOR)
    testArrays.append(config.ES + config.ISCH + config.FIMF + config.AB + config.HALBI)
    testArrays.append(config.ES + config.ISCH + config.FIMF + config.VOR + config.HALBI)
    testArrays.append(config.ES + config.ISCH + config.AINS)
    testArrays.append(config.ES + config.ISCH + config.ZWAI)
    testArrays.append(config.ES + config.ISCH + config.DREY)
    testArrays.append(config.ES + config.ISCH + config.VIERI)
    testArrays.append(config.ES + config.ISCH + config.FIMFI)
    testArrays.append(config.ES + config.ISCH + config.SAGGSI)
    testArrays.append(config.ES + config.ISCH + config.SIIBENI)
    testArrays.append(config.ES + config.ISCH + config.ACHTI)
    testArrays.append(config.ES + config.ISCH + config.NYYNI)
    testArrays.append(config.ES + config.ISCH + config.ZAANI)
    testArrays.append(config.ES + config.ISCH + config.ELFI)
    testArrays.append(config.ES + config.ISCH + config.ZWELFI)

    return testArrays

pixel_pin = board.D18
num_pixels = 114
order = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=order
)

print("start test")
resetLED()

color = config.DEFAULT_COLOR 

while True:
    tests = test()

    for i in tests:
        print("testing...")
        show(i, config.DEFAULT_COLOR)
        time.sleep(1)
