from flask import Flask, request, render_template
from collections import defaultdict
from flask_wtf import Form
from wtforms import FloatField

import comm_functions as comm
import adresse_lib as address_lib
import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x04
GPIO.setmode(GPIO.BCM)


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


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/button', methods=['GET', 'POST'])
def divide():

    class DivideForm(Form):
        numerator = FloatField("Number")
        denominator = FloatField("Divide by")

    form = DivideForm()
    result = None

    if form.validate_on_submit():
        but_val = request.form['submit']
        targetPins = address_lib.button_address[but_val]

        comm.simulate_send_address(targetPins, 1)

        if but_val == "B1":
            result = 1
        elif but_val == "B2":
            result = 2
        else:
            result = 2

    return render_template('button.html', result=result, form=form)


if __name__ == '__main__':
    app.run()
