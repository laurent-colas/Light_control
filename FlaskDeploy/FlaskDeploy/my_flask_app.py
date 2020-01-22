# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_thumbnails import Thumbnail

from wtforms import FloatField, StringField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request
import sqlite3 as sql
import threading
import db_functions as db_func
import threading

database_name = "home/pi/FlaskDeploy/FlaskDeploy/database.db"

app = Flask(__name__)

@app.before_first_request
def activate_job():
    def init_light_state():
        print("Initialisation of light states")
        db_func.init_light_state_db()
    thread = threading.Thread(target=init_light_state)
    thread.start()

class MacroForm(FlaskForm):
    choices = db_func.get_in_db('name', 'lights')
    macro_new_name = StringField('Name of macro', validators=[DataRequired()])
    switch_new_name = StringField('Name of switch (SWx)', validators=[DataRequired()])


@app.route('/enternewmacros')
def new_macro():
    form = MacroForm()
    choices = db_func.get_in_db('name', 'lights')
    return render_template('macros.html', form=form, choices=choices)

@app.route('/enternewswitch')
def new_switch():
    form = MacroForm()
    choices = db_func.get_in_db('name', 'macros')
    return render_template('switch.html', form=form, choices=choices)

@app.route('/list')
def list():
    rows = db_func.get_all_in_db("lights")

    return render_template("list.html", rows=rows)

@app.route('/switch_list')
def switch_list():
    form = MacroForm()
    rows = db_func.get_all_in_db("switch")
    # con = sqlite3.connect(database_name)
    #
    # cur = con.cursor()
    # cur.execute("select * from switch")
    # rows = cur.fetchall();
    return render_template("switch_list.html", rows=rows, form=form)

@app.route('/macros_list')
def macros_list():
    form = MacroForm()
    rows = db_func.get_all_in_db("macros")
    # con = sqlite3.connect(database_name)
    #
    # cur = con.cursor()
    # cur.execute("select * from macros")
    # rows = cur.fetchall();
    return render_template("macros_list.html", rows=rows, form=form)

@app.route('/add_macros', methods=['GET', 'POST'])
def add_macros():
    if request.method == 'POST':
        form = MacroForm()
        choices = db_func.get_all_places()
        macro_names = db_func.get_in_db('name', 'macros')

        new_macro_name = form.macro_new_name.data
        if new_macro_name in macro_names:
            new_macro_name = new_macro_name + "1"
        macro_places = request.form.getlist('room')

        db_func.add_macro(new_macro_name, macro_places)
        rows = db_func.get_all_in_db('macros')
        msg = "Macro successfully added"
        return render_template('macros_button.html', rows=rows, form=form)

@app.route('/add_switch', methods=['GET', 'POST'])
def add_switch():
    if request.method == 'POST':
        form = MacroForm()
        choices = db_func.get_all_places()
        switch_names = db_func.get_in_db('name', 'switch')

        new_switch_name = form.switch_new_name.data
        if new_switch_name in switch_names:
            new_switch_name = new_switch_name + "1"
        switch_places = request.form.getlist('room')

        db_func.add_switch(new_switch_name, switch_places)
        rows = db_func.get_all_in_db('switch')
        msg = "switch successfully added"
        return render_template('switch_list.html', rows=rows, form=form)

@app.route('/macros', methods=['GET', 'POST'])
def macros():
    form = MacroForm()
    if request.method == 'POST':
        macro_name = request.form['submit']
        macro_brightness = request.form[macro_name]
        db_func.change_macros_state(macro_brightness, macro_name)
    rows = db_func.get_all_in_db('macros')
    return render_template('macros_button.html', rows=rows, form=form)

@app.route('/', methods=['GET', 'POST'])
def all_lights():
    form = MacroForm()
    if request.method == 'POST':
        light_name = request.form['submit']
        light_brightness = request.form[light_name]
        db_func.change_light_state(light_brightness, light_name)
    rows = db_func.get_all_in_db('lights')
    return render_template('brightness_button.html', rows=rows, form=form)

@app.route('/SwitchDetector')
def switch_handler():
    switch_name = request.args.get('light', default='*', type=str)
    brightness = request.args.get('state', default=0, type=int)
    db_func.change_switch_state(switch_name, brightness)
    return "good"



if __name__ == '__main__':
    app.run()
