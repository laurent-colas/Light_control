import sqlite3
import csv



def create_db():
    con = sqlite3.connect('database.db')
    c = con.cursor()
    # get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='lights' ''')
    # if the count is 1, then table exists
    if c.fetchone()[0] == 1:
        print('Table exists.')
        c.execute('DROP TABLE lights');
    else:
        print('Table does not exist.')
    c1 = c.execute('PRAGMA encoding="UTF-8";')
    con.execute('CREATE TABLE lights (addr TEXT, name TEXT, brightness real, eol text)')
    c.close()
    con.close()


def create_macro_db():
    con = sqlite3.connect('database.db')
    c = con.cursor()
    # get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='macros' ''')
    # if the count is 1, then table exists
    if c.fetchone()[0] == 1:
        print('Table exists.')
        c.execute('DROP TABLE macros');
    else:
        print('Table does not exist.')
    c1 = c.execute('PRAGMA encoding="UTF-8";')
    con.execute('CREATE TABLE macros (name TEXT, brightness REAL, eol TEXT, places TEXT)')
    c.close()
    con.close()

def create_switch_db():
    con = sqlite3.connect('database.db')
    c = con.cursor()
    # get the count of tables with the name
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='switch' ''')
    # if the count is 1, then table exists
    if c.fetchone()[0] == 1:
        print('Table exists.')
        c.execute('DROP TABLE switch');
    else:
        print('Table does not exist.')
    c1 = c.execute('PRAGMA encoding="UTF-8";')
    con.execute('CREATE TABLE switch (name TEXT, brightness REAL, eol TEXT, macro TEXT)')
    c.close()
    con.close()

def init_db(data):
    con = sqlite3.connect('database.db')
    print("Opened database successfully");
    c = con.cursor()
    for i in range (0,len(data)):
        c.execute("INSERT INTO lights (addr,name,brightness,eol) VALUES(?, ?, ?, ?)", (data[i][0], data[i][1], data[i][2], data[i][3]))
        con.commit()
    c.close()
    con.close()

def init_macro_db(data):
    con = sqlite3.connect('database.db')
    print("Opened database successfully");
    c = con.cursor()
    for i in range (0,len(data)):
        c.execute("INSERT INTO macros (name,brightness,eol,places) VALUES(?, ?, ?, ?)", (data[i][0], data[i][1], data[i][2], data[i][3]))
        con.commit()
    c.close()
    con.close()

def init_switch_db(data):
    con = sqlite3.connect('database.db')
    print("Opened database successfully");
    c = con.cursor()
    for i in range(0, len(data)):
        c.execute("INSERT INTO switch (name,brightness,eol,macro) VALUES(?, ?, ?, ?)",
                  (data[i][0], data[i][1], data[i][2], data[i][3]))
        con.commit()
    c.close()
    con.close()

def read_csv(csv_file_name):
    with open(csv_file_name,  encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            print(f'\t addr: {row[0]} name: {row[1]} bright: {row[2]} eol: {row[3]} ')
            list_temp = [row[0], row[1], row[2], row[3]]
            data.append(list_temp)
            line_count += 1

        print(f'Processed {line_count} lines.')
        return data

def read_csv_macro(csv_file_name):
    with open(csv_file_name,  encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            print(f'\t name: {row[0]} bright: {row[1]} eol: {row[2]} lights: {row[3]} ')
            list_temp = [row[0], row[1], row[2], row[3]]
            data.append(list_temp)
            line_count += 1

        print(f'Processed {line_count} lines.')
        return data

def read_csv_switch(csv_file_name):
    with open(csv_file_name,  encoding="UTF-8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        data = []
        for row in csv_reader:
            print(f'\t name: {row[0]} bright: {row[1]} eol: {row[2]} macro name: {row[3]} ')
            list_temp = [row[0], row[1], row[2], row[3]]
            data.append(list_temp)
            line_count += 1

        print(f'Processed {line_count} lines.')
        return data


def update_db():
    data = []
    data = read_csv('scv_sans_acc/light_db.csv')
    create_db()
    init_db(data)

def update_macro_db():
    data = []
    data = read_csv_macro('scv_sans_acc/macro_db.csv')
    create_macro_db()
    init_macro_db(data)

def update_switch_db():
    data = []
    data = read_csv_macro('scv_sans_acc/switch_db.csv')
    create_switch_db()
    init_switch_db(data)

