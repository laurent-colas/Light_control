from flask import Flask, request, render_template
from collections import defaultdict
from flask_wtf import FlaskForm
from wtforms import FloatField

import comm_functions as comm
import adresse_lib as address_lib

'''
import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x04
GPIO.setmode(GPIO.BCM)

'''

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'


# http://192.168.0.106/MotionDetector?light=D1&state=1
@app.route('/MotionDetector')
def MotionHandler():
    light = request.args.get('light', default='*', type=str)
    state = request.args.get('state', default=2, type=int)

    targetPins = address_lib.motion_detect_address[light]

    comm.send_address(bus, address, targetPins, state)

    return 'Motion Detected from ESP8266'


# http://192.168.0.106/ButtonDetector?light=B1&state=1
@app.route('/ButtonDetector')
def ButtonHandler():
    light = request.args.get('light', default='*', type=str)
    state = request.args.get('state', default=2, type=int)

    # link between the physical button and relay address
    targetPins = address_lib.button_address[light]

    comm.send_address(bus, address, targetPins, state)

    return 'Button pressed by ESP8266'


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'


@app.route('/', methods=['GET', 'POST'])
def divide():

    class DivideForm(FlaskForm):
        numerator = FloatField("Number")
        denominator = FloatField("Divide by")

    form = DivideForm()
    result = None

    list_places =address_lib.places_name



    if form.validate_on_submit():
        #   receive
        light_address = request.form['submit']
        # light_address = but_val

        # light_address_name = request.form['place']

        # light_address = but_val[0:2]
        # light_state = but_val[2:]
        # test = but_val[3:]

        light_state = 3

        for key in list_places.keys():
            if light_address == key:
                target_pins = list_places[key]
                address_key = key
                if target_pins[0] == 1:
                    list_places[key][0] = 0
                else:
                    list_places[key][0] = 1

                #
                # if list_places[key] == 1:
                #     list_places[key] = 0
                #     light_state = 0
                # else:
                #     list_places[key] = 1
                #     light_state = 1

        result = 3
        # targetPins = address_lib.button_address[light_address]
        final_target_pins = list_places[light_address][1:]
        final_state = list_places[light_address][0]

        comm.simulate_send_address(final_target_pins, final_state)
        # if light_address == "B1":
        #     result = 1
        # elif light_address == "B2":
        #     result = 2
        # else:
        #     result = 3




    return render_template('button.html',list_places=list_places, form=form)


if __name__ == '__main__':
    app.run()

