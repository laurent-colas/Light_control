from __future__ import unicode_literals
from flask import Flask, request, render_template
from flask_wtf import FlaskForm

from wtforms import FloatField, StringField
from wtforms.validators import DataRequired

import logging
import csv
import comm_functions as comm
import adresse_lib as address_lib
import threading
import Adafruit_PCA9685


import RPi.GPIO as GPIO
import smbus

bus = smbus.SMBus(1)
# This is the address we setup in the Arduino Program
# Slave Address 1
address = 0x05
GPIO.setmode(GPIO.BCM)



app = Flask(__name__)
app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'

# configs.init_macro_csv()
# with app.app_context():
#     init_macro_csv()

pwm = Adafruit_PCA9685.PCA9685()
pwm_freq = 500
pwm.set_pwm_freq(pwm_freq)


# @app.before_first_request
# def activate_job():
#     def init_macro_csv():
#         print("Loading Macros")
#         macro_list_name = address_lib.macros_names
#         with open('macro_list.csv') as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
#             for row in csv_reader:
#                 macro_place_list_temp = row[1:]
#                 macro_place_list_temp.insert(0, 0)
#                 macro_list_name[row[0]] = macro_place_list_temp
#                 print(row[0])
#                 print(macro_list_name[row[0]])
#     thread = threading.Thread(target=init_macro_csv)
#     thread.start()


# # http://192.168.0.106/MotionDetector?light=D1&state=1
# @app.route('/MotionDetector')
# def motion_handler():
#     light = request.args.get('light', default='*', type=str)
#     state = request.args.get('state', default=0, type=int)
#
#     target_place = address_lib.motion_detect_address[light]
#
#     if type(target_place) is list:
#         for place in target_place:
#             final_target_pins = address_lib.places_name[place]
#             address_lib.places_name[place][0] = state
#             comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[place][0])
#             comm.send_address_brightness(pwm, final_target_pins[1:], address_lib.places_name[place][0])
#     else:
#         final_target_pins = address_lib.places_name[target_place]
#         address_lib.places_name[target_place][0] = state
#         comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[target_place][0])
#         comm.send_address_brightness(pwm, final_target_pins[1:], address_lib.places_name[target_place][0])
#
#     return 'Motion Detected from ESP8266'


# http://192.168.0.106/MotionDetector?light=D1&state=1
@app.route('/MotionDetector')
def motion_handler():
    light = request.args.get('light', default='*', type=str)
    state = request.args.get('state', default=0, type=int)

    target_place = address_lib.motion_detect_address[light]

    if type(target_place) is list:
        for place in target_place:
            final_target_pins = address_lib.places_name[place]
            address_lib.places_name[place][0] = state
            comm.simulate_send_address_brightness(final_target_pins[1:], address_lib.places_name[place][0])
            comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins[1:], address_lib.places_name[place][0])
    else:
        final_target_pins = address_lib.places_name[target_place]
        address_lib.places_name[target_place][0] = state
        comm.simulate_send_address_brightness(final_target_pins[1:], address_lib.places_name[target_place][0])
        comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins[1:], address_lib.places_name[target_place][0])

    return_string = 'Motion at ' + light
    return return_string



# # http://192.168.0.106/ButtonDetector?light=B1&state=1
# @app.route('/ButtonDetector')
# def button_handler():
#     light = request.args.get('light', default='*', type=str)
#     state = request.args.get('state', default=0, type=int)
#
#     # link between the physical button and relay address
#
#     target_place = address_lib.button_address[light]
#     if type(target_place) is list:
#         for place in target_place:
#             final_target_pins = address_lib.places_name[place]
#             address_lib.places_name[place][0] = state
#             comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[place][0])
#             comm.send_address_brightness(pwm, final_target_pins[1:], address_lib.places_name[place][0])
#     else:
#         final_target_pins = address_lib.places_name[target_place]
#         address_lib.places_name[target_place][0] = state
#         comm.simulate_send_address(final_target_pins[1:], address_lib.places_name[target_place][0])
#         comm.send_address_brightness(pwm, final_target_pins[1:], address_lib.places_name[target_place][0])
#
#     return 'Button pressed by ESP8266'


# http://192.168.0.106/ButtonDetector?light=B1&state=1
@app.route('/ButtonDetector')
def button_handler():
    light = request.args.get('light', default='*', type=str)
    state = request.args.get('state', default=0, type=int)

    # link between the physical button and relay address

    target_place = address_lib.button_address[light]
    if type(target_place) is list:
        for place in target_place:
            final_target_pins = address_lib.places_name[place]
            address_lib.places_name[place][0] = state
            comm.simulate_send_address_brightness(final_target_pins[1:], address_lib.places_name[place][0])
            comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins[1:],
                                               address_lib.places_name[place][0])
    else:
        final_target_pins = address_lib.places_name[target_place]
        address_lib.places_name[target_place][0] = state
        comm.simulate_send_address_brightness(final_target_pins[1:], address_lib.places_name[target_place][0])
        comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins[1:],
                                           address_lib.places_name[target_place][0])

    return 'Button pressed by ESP8266'


# # http://192.168.0.106/BrightnessButtonDetector?light=B1&brightness=100
# @app.route('/BrightnessButtonDetector')
# def bright_button_handler():
#     light = request.args.get('light', default='*', type=str)
#     brightness = request.args.get('brightness', default=0, type=int)
#
#     target_place = address_lib.button_address[light]
#     print('target places: ' + target_place)
#     if type(target_place) is list:
#         for place in target_place:
#             final_target_pins = address_lib.places_name[place][1:]
#             address_lib.places_name[place][0] = brightness
#
#             comm.simulate_send_address_brightness(final_target_pins,
#                                                   address_lib.places_name[place][0])
#             comm.send_address_brightness(pwm, final_target_pins, address_lib.places_name[place][0])
#     else:
#         final_target_pins = address_lib.places_name[target_place][1:]
#         address_lib.places_name[target_place][0] = brightness
#         comm.simulate_send_address_brightness(final_target_pins,
#                                               address_lib.places_name[target_place][0])
#         comm.send_address_brightness(pwm, final_target_pins, address_lib.places_name[target_place][0])
#
#     return 'Intensity Button pressed by ESP8266'



# http://192.168.0.106/BrightnessButtonDetector?light=B1&brightness=100
@app.route('/BrightnessButtonDetector')
def bright_button_handler():
    light = request.args.get('light', default='*', type=str)
    brightness = request.args.get('brightness', default=0, type=int)

    target_place = address_lib.button_address[light]

    if type(target_place) is list:
        # target_place = address_lib.places_name_brightness[light]
        for place in target_place:
            final_target_pins = address_lib.places_name[place][1:]
            address_lib.places_name[place][0] = brightness
            comm.simulate_send_address_brightness(final_target_pins, address_lib.places_name[place][0])
            comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins,
                                               address_lib.places_name[place][0])
            # comm.send_address_brightness(pwm, final_target_pins, address_lib.places_name_brightness[place][0])
    else:
        final_target_pins = address_lib.places_name[target_place][1:]
        address_lib.button_address[target_place][0] = brightness
        comm.simulate_send_address_brightness(final_target_pins, address_lib.places_name[target_place][0])
        comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins,
                                           address_lib.places_name[target_place][0])
        # comm.send_address_brightness(pwm, final_target_pins, address_lib.places_name_brightness[target_place][0])

    return 'Intensity Button pressed by ESP8266'



@app.route('/hello')
def hello_world():
    return 'Hello World'


class DivideForm(FlaskForm):
    numerator = FloatField("Number")
    denominator = FloatField("Divide by")


class MacroForm(FlaskForm):
    choices = list(address_lib.places_name.keys())
    macro_new_name = StringField('Name of macro', validators=[DataRequired()])


class BrightnessForm(FlaskForm):
    choices = list(address_lib.places_name.keys())


class ButtonForm(FlaskForm):
    choices = list(address_lib.button_address.keys())


class DetectorForm(FlaskForm):
    choices = list(address_lib.motion_detect_address.keys())


@app.route('/add_macros', methods=['GET', 'POST'])
def add_macros():
    form = MacroForm()
    button_form = DivideForm()
    choices = list(address_lib.places_name.keys())
    if form.validate():
        macro_list_name = address_lib.macros_names
        name_new_macro = form.macro_new_name.data
        if name_new_macro in address_lib.macros_names:
            name_new_macro = name_new_macro + "1"
        macro_places = request.form.getlist('room')
        macro_places.insert(0, 0)
        macro_list_name[name_new_macro] = macro_places

        with open('macro_list.csv', mode='a', newline='') as macro_list_file:
            print("Writing new macro info")
            test = macro_places[1:]
            test.insert(0, name_new_macro)
            writer = csv.writer(macro_list_file, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writerow(test)

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

        if list_of_imp_macro[0] >= 1:
            list_of_imp_macro[0] = 0
        else:
            list_of_imp_macro[0] = 100

        for place in list_of_imp_macro[1:]:
            list_places[place][0] = list_of_imp_macro[0]

            final_target_pins = address_lib.places_name[place][1:]
            final_state = address_lib.places_name[place][0]
            comm.simulate_send_address_brightness(final_target_pins, final_state)
            comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins,final_state)

        # for i in range(1, len(list_of_imp_macro)):
        #     for key in list_places.keys():
        #         if list_of_imp_macro[i] == key:
        #             list_places[key][0] = list_of_imp_macro[0]
        #             final_target_pins = list_places[list_of_imp_macro[i]][1:]
        #             final_state = list_places[list_of_imp_macro[i]][0]
        #             comm.simulate_send_address(final_target_pins, final_state)
        #             print('final target pin: ' + str(final_target_pins))
        #             print('final state: ' + str(final_state))
        #             comm.send_address_brightness(pwm, final_target_pins, final_state)

    return render_template('macros_button.html', list_macros=macro_list_name, form=button_form)


@app.route('/brightness', methods=['GET', 'POST'])
def brightness_button():

    # get
    form = BrightnessForm()
    list_places = address_lib.places_name

    if form.validate_on_submit():
        light_address = request.form['submit']
        light_address_brightness = request.form[light_address]
        print('brightness: ' + str(light_address_brightness))
        list_places[light_address][0] = int(light_address_brightness)

        final_target_pins = list_places[light_address][1:]
        final_state = address_lib.places_name[light_address][0]
        comm.simulate_send_address_brightness(final_target_pins, final_state)
        comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins, final_state)

        # comm.simulate_send_address(final_target_pins, final_state)
        # print('hello')
        # print(final_target_pins)
        # print(final_state)
        # comm.send_address_brightness(pwm, final_target_pins, final_state)

    return render_template('brightness_button.html', list_places=list_places, form=form)

@app.route('/buttons', methods=['GET', 'POST'])
def button_map():
    form = ButtonForm()
    list_buttons = address_lib.button_address

    return render_template('buttons_page.html', list_buttons=list_buttons, form=form)


@app.route('/motiondetector', methods=['GET', 'POST'])
def detector_map():
    form = DetectorForm()
    list_detectors = address_lib.motion_detect_addresses

    return render_template('motion_page.html', list_buttons=list_detectors, form=form)

# @app.route('/relaycodes', methods=['GET', 'POST'])
# def relay_codes():
#
#     form = DivideForm()
#     list_places = address_lib.places_name
#     if form.validate_on_submit():
#
#         light_address = request.form['submit']
#         print('Light address: ' + light_address)
#         target_pins = address_lib.places_name[light_address]
#         if target_pins[0] >= 1:
#             address_lib.places_name[light_address][0] = 0
#         else:
#             address_lib.places_name[light_address][0] = 100
#
#         final_target_pins = address_lib.places_name[light_address][1:]
#         final_state = address_lib.places_name[light_address][0]
#         comm.simulate_send_address_brightness(final_target_pins, final_state)
#         comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins, final_state)

        # print('probleme: ' + str(address_lib.places_name[light_address][0]))
        # if int(address_lib.places_name[light_address][0]) >= 1:
        #     address_lib.places_name[light_address][0] = 0
        # else:
        #     address_lib.places_name[light_address][0] = 100
        #
        # comm.simulate_send_address(final_target_pins, address_lib.places_name[light_address][0])
        # comm.send_address_brightness(pwm, final_target_pins, list_places[light_address][0])

        # for key in list_places.keys():
        #     if light_address == key:
        #         target_pins = list_places[key]
        #         print(target_pins)
        #         if target_pins[0] >= 1:
        #             list_places[key][0] = 0
        #         else:
        #             list_places[key][0] = 100

        # final_target_pins = list_places[light_address][1:]
        # final_state = list_places[light_address][0]
        # comm.simulate_send_address(final_target_pins, final_state)
        # comm.send_address_brightness(pwm, final_target_pins, list_places[light_address][0])
    # print('done')
    # return render_template('relay_page.html', list_places=list_places, form=form)


@app.route('/', methods=['GET', 'POST'])
def divide():

    form = DivideForm()
    list_places = address_lib.places_name
    if form.validate_on_submit():

        light_address = request.form['submit']
        print('Light address: ' + light_address)
        target_pins = address_lib.places_name[light_address]
        if target_pins[0] >= 1:
            address_lib.places_name[light_address][0] = 0
        else:
            address_lib.places_name[light_address][0] = 100

        final_target_pins = address_lib.places_name[light_address][1:]
        final_state = address_lib.places_name[light_address][0]
        comm.simulate_send_address_brightness(final_target_pins, final_state)
        comm.send_mixed_address_brightness(bus, address, pwm, final_target_pins, final_state)

        # print('probleme: ' + str(address_lib.places_name[light_address][0]))
        # if int(address_lib.places_name[light_address][0]) >= 1:
        #     address_lib.places_name[light_address][0] = 0
        # else:
        #     address_lib.places_name[light_address][0] = 100
        #
        # comm.simulate_send_address(final_target_pins, address_lib.places_name[light_address][0])
        # comm.send_address_brightness(pwm, final_target_pins, list_places[light_address][0])

        # for key in list_places.keys():
        #     if light_address == key:
        #         target_pins = list_places[key]
        #         print(target_pins)
        #         if target_pins[0] >= 1:
        #             list_places[key][0] = 0
        #         else:
        #             list_places[key][0] = 100

        # final_target_pins = list_places[light_address][1:]
        # final_state = list_places[light_address][0]
        # comm.simulate_send_address(final_target_pins, final_state)
        # comm.send_address_brightness(pwm, final_target_pins, list_places[light_address][0])
    print('done')
    return render_template('button.html', list_places=list_places, form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
