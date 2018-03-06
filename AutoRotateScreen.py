#!/usr/bin/env python

import subprocess
from subprocess import check_call, check_output
import time

orientation = ["normal", "inverted", "left", "right"]
statePrev = -1

# set your touchscreen and touchpad names here, see xinput's output
touchscreen = "ELAN2514:00 04F3:259B"
touchpad = "SynPS/2 Synaptics TouchPad"

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

        if orientation[state] == "normal":
            transval = "1 0 0 0 1 0 0 0 1"
        if orientation[state] == "left" :
            transval = "0 -1 1 1 0 0 0 0 1"
        if orientation[state] == "right" :
            transval = "0 1 0 -1 0 1 0 0 1"
        if orientation[state] == "inverted":
            transval = "-1 0 1 0 -1 1 0 0 1"

        if touchscreen != "":
            check_call(['xinput', 'set-prop', touchscreen, 'Coordinate Transformation Matrix'] + transval.split())

        if touchpad != "":
            check_call(['xinput', 'set-prop', touchpad, 'Coordinate Transformation Matrix'] + transval.split())

    statePrev = state
    time.sleep(1)

