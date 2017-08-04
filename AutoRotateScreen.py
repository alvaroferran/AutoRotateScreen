#!/usr/bin/env python

import subprocess
import time

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
            subprocess.call(["xrandr", "-o", "normal"])
        else:
            subprocess.call(["xrandr", "-o", "inverted"])

    if abs(angleY) > abs(angleX) + buffer:
        if angleY >= 0:
            subprocess.call(["xrandr", "-o", "left"])
        else:
            subprocess.call(["xrandr", "-o", "right"])

    time.sleep(1)

