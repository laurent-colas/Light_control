# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import constant as const
import Adafruit_PCA9685
from datetime import datetime
logfile_name = "home/pi/FlaskDeploy/FlaskDeploy/log_file.txt"
import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)
GPIO.setmode(GPIO.BCM)
#
# pwm1 = Adafruit_PCA9685.PCA9685(const.address_pwm_1)
# pwm2 = Adafruit_PCA9685.PCA9685(const.address_pwm_2)
# pwm3 = Adafruit_PCA9685.PCA9685(const.address_pwm_3)
pwm4 = Adafruit_PCA9685.PCA9685(const.address_pwm_4)
pwm_freq = 500
# pwm1.set_pwm_freq(pwm_freq)
# pwm2.set_pwm_freq(pwm_freq)
# pwm3.set_pwm_freq(pwm_freq)
pwm4.set_pwm_freq(pwm_freq)

def string_to_bytes(val):
    ret_val = []
    for c in val:
        ret_val.append(ord(c))
    return ret_val

def write_number(relay_address, value):
    bus.write_byte(relay_address, value)
    return -1


def send_light_state(adresse, brightness):
    if adresse[0] == "A":
        send_pwm_light_state(adresse, brightness)
    else:
        send_relay_light_state(adresse, brightness)


def send_pwm_light_state(adresse, brightness):
    address_num = int(adresse[1:])
    pwm_brightness_off = int((int(brightness) / 100) * 4095)

    if address_num <= 15:
        pwm_address = const.address_pwm_1
        pwm1.set_pwm(adj_address_num, 0, pwm_brightness_off)
    elif address_num >= 16 and address_num < 32:
        pwm_address = const.address_pwm_2
        adj_address_num = address_num - 16
        pwm2.set_pwm(adj_address_num, 0, pwm_brightness_off)
    elif address_num >= 32 and address_num < 48:
        pwm_address = const.address_pwm_3
        adj_address_num = address_num - 32
        pwm3.set_pwm(adj_address_num, 0, pwm_brightness_off)
    elif address_num >= 48 and address_num < 64:
        pwm_address = const.address_pwm_4
        adj_address_num = address_num - 48
        pwm4.set_pwm(adj_address_num, 0, pwm_brightness_off)
    message = "PWM controler address: ", hex(pwm_address), "at address: ", adj_address_num, " with pwm at: ", pwm_brightness_off
    print(message)

def send_relay_light_state(adress, brightness):
    command = create_relay_string(adress, brightness)
    message = "Relay state change: ", command
    print(message)


def create_relay_string(address, brightness):
    if int(brightness) <= 10:
        brightness = 0
    else:
        brightness = 1
    command = address + " " + str(brightness)
    return command

def eprint(message):
    sample = open(logfile_name, 'a')
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    message = str(dt_string) + " : "+ str(message)
    print(message, file=sample)
    sample.close()


def print_first_boot():
    message = "--------------------------------------"
    eprint(message)
    message = "First boot light state"
    eprint(message)
    message = "--------------------------------------"
    eprint(message)