#!/usr/bin/env python

import time

from gpiozero import Button

import board
import neopixel
import numpy as np

pixel_pin = board.D18
num_pixels = 114
order = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.0, auto_write=False, pixel_order=order
)





def wheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if order in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


while True:
    pixels.fill((255, 0, 255))
    pixels.show()
    time.sleep(1)

    pixels.fill((0, 255, 0))

    pixels.show()
    time.sleep(1)

    pixels.fill((0, 0, 255))

    pixels.show()
    time.sleep(1)

#     rainbow_cycle(0.001)
