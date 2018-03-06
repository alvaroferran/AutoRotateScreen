#!/usr/bin/env python

import subprocess
from subprocess import check_call, check_output
import time

# Enable touchpad rotation by uncommenting the following line.
# touchpad = "SynPS/2 Synaptics TouchPad"

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
            transval = "1 0 0 0 1 0 0 0 1"
        else:
            state = 1
            transval = "-1 0 1 0 -1 1 0 0 1"

    if abs(angleY) > abs(angleX) + buffer:
        if angleY >= 0:
            state = 2
            transval = "0 -1 1 1 0 0 0 0 1"
        else:
            state = 3
            transval = "0 1 0 -1 0 1 0 0 1"

    if state != statePrev:
        subprocess.call(["xrandr", "-o", orientation[state]])
        if 'touchpad' in globals():
            check_call(['xinput', 'set-prop', touchpad,
                        'Coordinate Transformation Matrix'] + transval.split())

    statePrev = state
    time.sleep(1)

