from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

pwm_max = 4096
pwm_min = 0
pwm_freq = 300

pwm.set_pwm_freq(pwm_freq)

def send_address_brightness(pwm, target_pins, brightness):
    pwm_brightness_off = int((brightness / 100) * 4096)
    print(pwm_brightness_off)
    pwm.set_pwm(target_pins, 0, pwm_brightness_off)



while True:

    for led in range(0, 3):
        # pwm.set_pwm(led, 0, 4095)
        # time.sleep(1)
        # print(led)
        # pwm.set_pwm(led, 0, 1)
        for i in range(0, 100, 1):
            send_address_brightness(pwm, led, i)
            # pwm.set_pwm(led, 0, i)
            # time.sleep(0.001)
        for i in range(100, 0, -1):
            send_address_brightness(pwm, led, i)
            # time.sleep(0.001)
