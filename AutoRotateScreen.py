#!/usr/bin/env python

import subprocess
import time

orientation = ["normal", "inverted", "left", "right"]
statePrev = -1

# Buffer value to increase hysteresis if needed
buffer = 0

while True:

    angleX = subprocess.check_output(
             "cat /sys/bus/iio/devices/iio:device*/in_incli_x_raw", shell=True)
    angleY = subprocess.check_output(
             "cat /sys/bus/iio/devices/iio:device*/in_incli_y_raw", shell=True)

    angleX = int(angleX)
    angleY = int(angleY)

    if abs(angleY) < abs(angleX) - buffer:
        if angleX >= 0:
            state = 0
        else:
            state = 1

    if abs(angleY) > abs(angleX) + buffer:
        if angleY >= 0:
            state = 2
        else:
            state = 3

    if state != statePrev:
        subprocess.call(["xrandr", "-o", orientation[state]])

    statePrev = state
    time.sleep(1)

