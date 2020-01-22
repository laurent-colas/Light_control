from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685(0x40)

pwm_max = 4096
pwm_min = 0
pwm_freq = 300

pwm.set_pwm_freq(pwm_freq)


while True:
    for led in range(0, 2):
        for i in range(pwm_min, pwm_max, 8):
            pwm.set_pwm(led, 0, i)
            time.sleep(0.001)
        for i in range(pwm_max, pwm_min, -8):
            pwm.set_pwm(led, 0, i)
            time.sleep(0.001)
