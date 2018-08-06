from flask import Flask, request, render_template
# from collections import defaultdict
from flask_wtf import FlaskForm

from wtforms import FloatField, StringField
from wtforms.validators import DataRequired
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
def motion_handler():
    light = request.args.get('light', default='*', type=str)
    # state = request.args.get('state', default=0, type=int)

    target_place = address_lib.motion_detect_address[light]
    final_target_pins = address_lib.places_name[target_place]

    if final_target_pins[0] == 1:
        address_lib.places_name[target_place][0] = 0
    else:
        address_lib.places_name[target_place][0] = 1
    comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[target_place][0])

    # comm.send_address(bus, address, targetPins, state)

    return 'Motion Detected from ESP8266'


# http://192.168.0.106/ButtonDetector?light=B1&state=1
@app.route('/ButtonDetector')
def button_handler():
    light = request.args.get('light', default='*', type=str)
    # state = request.args.get('state', default=0, type=int)

    # link between the physical button and relay address
    target_place = address_lib.button_address[light]
    final_target_pins = address_lib.places_name[target_place]

    if final_target_pins[0] == 1:
        address_lib.places_name[target_place][0] = 0
    else:
        address_lib.places_name[target_place][0] = 1

    comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[target_place][0])
    # targetPins = address_lib.button_address[light]
    #
    # comm.send_address(bus, address, targetPins, state)
    return 'Button pressed by ESP8266'


@app.route('/hello_world')
def hello_world():
    return 'Hello World!'


class DivideForm(FlaskForm):
    numerator = FloatField("Number")
    denominator = FloatField("Divide by")


class MacroForm(FlaskForm):
    choices = list(address_lib.places_name.keys())
    macro_new_name = StringField('Name of macro', validators=[DataRequired()])


@app.route('/add_macros', methods=['GET', 'POST'])
def add_macros():
    form = MacroForm()
    button_form = DivideForm()
    choices = list(address_lib.places_name.keys())
    # list_places = address_lib.places_name
    if form.validate():
        macro_list_name = address_lib.macros_names
        name_new_macro = form.macro_new_name.data
        macro_places = request.form.getlist('room')
        macro_places.insert(0, 0)
        macro_list_name[name_new_macro] = macro_places
        return render_template('macros_button.html', list_macros=macro_list_name, form=button_form)
    return render_template('macros.html', form=form, choices=choices)


@app.route('/macros', methods=['GET', 'POST'])
def macros():
    button_form = DivideForm()
    macro_list_name = address_lib.macros_names
    list_places = address_lib.places_name

    if button_form.validate_on_submit():
        macro_name = request.form['submit']
        list_of_imp_macro = macro_list_name[macro_name]

        if list_of_imp_macro[0] == 1:
            list_of_imp_macro[0] = 0
        else:
            list_of_imp_macro[0] = 1

        for key in list_places.keys():
            for i in range(1, len(list_of_imp_macro)):
                if list_of_imp_macro[i] == key:
                    list_places[key][0] = list_of_imp_macro[0]

                final_target_pins = list_places[list_of_imp_macro[i]][1:]
                final_state = list_places[list_of_imp_macro[i]][0]
                comm.simulate_send_address(final_target_pins, final_state)

    return render_template('macros_button.html', list_macros=macro_list_name, form=button_form)


@app.route('/', methods=['GET', 'POST'])
def divide():

    form = DivideForm()
    list_places = address_lib.places_name
    if form.validate_on_submit():
        #   receive
        light_address = request.form['submit']

        for key in list_places.keys():
            if light_address == key:
                target_pins = list_places[key]
                if target_pins[0] == 1:
                    list_places[key][0] = 0
                else:
                    list_places[key][0] = 1

        final_target_pins = list_places[light_address][1:]
        final_state = list_places[light_address][0]
        comm.simulate_send_address(final_target_pins, final_state)

    return render_template('button.html', list_places=list_places, form=form)


if __name__ == '__main__':
    app.run()
