# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sqlite3
import csv
import comm_functions

database_name = "home/pi/FlaskDeploy/FlaskDeploy/database.db"
# cd
# etc / apache2 / sites - available /



def connect_db():
    con = sqlite3.connect(database_name)
    print("Opened database successfully");
    c = con.cursor()
    return con, c


def init_light_state_db():
    comm_functions.print_first_boot()
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        c.execute("SELECT * FROM lights")
        rows = c.fetchall()
        for i in range(1,len(rows)):
            if rows[i][2] > 0:
                address = rows[i][0]
                brightness = rows[i][2]
                comm_functions.send_light_state(address, brightness)
                message = "First: Update " + str(rows[i][0]) + " to brightness " + str(brightness)
                comm_functions.eprint(message)
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
            # print("The SQLite connection is closed")

def change_light_state(brightness, address):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        command = "UPDATE lights SET brightness = " + str(brightness) +" WHERE name = " + str(address)
        print(command)

        c.execute("update lights set brightness = ? where name = ?",(brightness, address))
        con.commit()
        num_address = get_addr_from_name(con, c, address)
        comm_functions.send_light_state(num_address, brightness)
        comm_functions.eprint(command)
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
            # print("The SQLite connection is closed")

def change_macros_state(brightness, name):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        sql_update_query = "UPDATE macros SET brightness = " + brightness + " WHERE name = " + name
        print(sql_update_query)
        c.execute("UPDATE macros SET brightness = ? WHERE name = ?",(brightness, name))
        con.commit()
        message = "Update " + name + " to brightness " + str(brightness)
        comm_functions.eprint(message)

        # get places for macro
        c.execute("SELECT * FROM macros WHERE name=?", (name,))
        print(name)
        rows = c.fetchall()
        if len(rows) == 0:
            print("Macro not found")
        else:
            places = rows[0][3].split(" ")
            for light in places:
                c.execute("UPDATE lights SET brightness = ? WHERE addr= ?",(brightness, light))
                con.commit()
                comm_functions.send_light_state(light, brightness)
                message = "Update " + light + " to brightness " + str(brightness)
                print(message)
                comm_functions.eprint(message)
        c.close()
    except sqlite3.Error as error:
        print("Failed to update mmmmmmmmmm sqlite table", error)
    finally:
        if (con):
            con.close()
            # print("The SQLite connection is closed")

def change_switch_state(switch_name, brightness):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        sql_update_query = """Update switch set brightness = ? where name = ?"""
        data = (brightness, switch_name)
        c.execute(sql_update_query, data)
        con.commit()
        message = "Update Switch " + switch_name + " to brightness " + str(brightness)
        comm_functions.eprint(message)

        # get places for macro
        c.execute("SELECT * FROM switch WHERE name=?", (switch_name,))
        rows = c.fetchall()
        macro_name = rows[0][3]

        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (con):
            con.close()
    change_macros_state(brightness, macro_name)


def get_addr_from_name(con, c, name):
    c.execute("SELECT * FROM lights WHERE name=?", (name,))
    rows = c.fetchall()
    address = rows[0][0]
    return address

def get_name_from_addr(con, c, addr):
    c.execute("SELECT * FROM lights WHERE addr=?", (addr,))
    rows = c.fetchall()
    name = rows[0][1]
    return rows

def add_macro(macro_name, places):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        places_string = ""
        if type(places) is list:
            for place in places:
                address = get_addr_from_name(con, c, place)
                places_string += address + " "
            places_string = places_string[0:-1]
        else:
            address = get_addr_from_name(con, c, places)
            places_string += address
        c.execute("INSERT INTO macros (name,brightness,eol,places) VALUES(?, ?, ?, ?)",
                  (macro_name, 0, "NA", places_string))
        con.commit()
        print("Macro: " + macro_name + " added to db")
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (con):
            con.close()
            # print("The SQLite connection is closed")

def add_switch(switch_name, macro_name):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        places_string = ""
        c.execute("INSERT INTO switch (name,brightness,eol,macro) VALUES(?, ?, ?, ?)",
                  (switch_name, 0, "NA", macro_name[0]))
        con.commit()
        comm_functions.eprint("Switch: " + switch_name + " added to db, linked to :" + macro_name[0])
        c.close()
    except sqlite3.Error as error:
        print("Failed to update sqlite table", error)
    finally:
        if (con):
            con.close()



def get_all_places():
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        c.execute("SELECT name FROM lights")
        rows = c.fetchall()
        list_places = []
        for i in range(1,len(rows)):
            list_places.append(rows[i][0])
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()

    return list_places

def get_name_macros():
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        c.execute("SELECT name FROM macros")
        rows = c.fetchall()
        list_macros = []
        for i in range(1,len(rows)):
            list_macros.append(row[i][0])
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
    return list_macros

def get_in_db(column_name, table_name):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        command = "SELECT " + column_name + " FROM " + table_name
        c.execute(command)
        rows = c.fetchall()
        list = []
        for i in range(1,len(rows)):
            list.append(rows[i][0])
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
    return list

def get_all_in_db(table_name):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        command = "SELECT * FROM " + table_name
        c.execute(command)
        rows = c.fetchall()
        list = rows[1:]
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
    return list

def get_name_from_macro(rows):
    try:
        con = sqlite3.connect(database_name)
        c = con.cursor()
        linked_names = []
        name_per_macro = []
        for row in rows:
            print(row[3])
            addresses = row[3].split(" ")
            for address in addresses:
                name = get_name_from_addr(con, c, address)
                name_per_macro.append(name[0][1])
            linked_names.append(name_per_macro)
            name_per_macro = []
        c.close()
    except sqlite3.Error as error:
        message = "Failed to update sqlite table", error
        print(message)
    finally:
        if (con):
            con.close()
    return linked_names
