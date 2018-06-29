from flask import Flask, request

import RPi.GPIO as GPIO
import logging
from collections import defaultdict

import smbus
import time
import sys

import isodate

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x04
GPIO.setmode(GPIO.BCM)

app = Flask(__name__)

def write_number(value):
    bus.write_byte(address, value)
    # bus.write_byte(address_2, value)
    # bus.write_byte_data(address, 0, value)
    return -1


def read_number():
    # number = bus.read_byte(address)
    number = bus.read_byte_data(address, 1)
    return number


def string_to_bytes(val):
    ret_val = []
    for c in val:
        ret_val.append(ord(c))
    return ret_val




@app.route('/helloesp')
def helloHandler():
	return 'Hello ESP8266, from Flask'

@app.route('/MotionDetector')
def MotionHandler():
	light = request.args.get('light', default = '*', type = str)
	state = request.args.get('state', default = 2, type = int)
	print(light);
	print(state);
	# http://192.168.0.106/MotionDetector?light=livingroom&state=1

	locationDict = defaultdict(list)
	locationDict = {
		'fan': ['A01','A02'],
		'light': ['A03','A04']
	}

	targetPins = locationDict[light]
	for i in range(len(targetPins)):
		command = "%s %d" % (targetPins[i], state)
		data_list = list(string_to_bytes(command))
		for j in data_list :
			write_number(j)
			time.sleep(.1)
		time.sleep(0.5)

    	return 'Hello ESP8266, from Flask'

@app.route('/ButtonDetector')
def ButtonHandler():
        light = request.args.get('light', default = '*', type = str)
        state = request.args.get('state', default = 2, type = int)
        print(light);
        print(state);
        # http://192.168.0.106/MotionDetector?light=livingroom&state=1

        locationDict = defaultdict(list)
        locationDict = {
                'fan': ['A01','A02'],
                'light': ['A03','A04']
        }

        targetPins = locationDict[light]
        for i in range(len(targetPins)):
                command = "%s %d" % (targetPins[i], state)
                data_list = list(string_to_bytes(command))
                for j in data_list :
                        write_number(j)
                        time.sleep(.1)
                time.sleep(0.5)

        return 'Hello ESP8266, from Flask'


app.run(host='0.0.0.0', port= 8090)


