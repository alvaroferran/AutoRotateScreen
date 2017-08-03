#!/usr/bin/python

import os
import commands
import time

# Buffer value to increase hysteresis if needed
buffer = 0

while True:

    angleX = commands.getoutput(
             'cat /sys/bus/iio/devices/iio\:device*/in_incli_x_raw')
    angleY = commands.getoutput(
             'cat /sys/bus/iio/devices/iio\:device*/in_incli_y_raw')

    angleX = int(angleX)
    angleY = int(angleY)

    if abs(angleY) < abs(angleX) - buffer:
        if angleX >= 0:
            os.system('xrandr -o normal')
        else:
            os.system('xrandr -o inverted')

    if abs(angleY) > abs(angleX) + buffer:
        if angleY >= 0:
            os.system('xrandr -o left')
        else:
            os.system('xrandr -o right')

    time.sleep(1)
