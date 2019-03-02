import csv
import adresse_lib as address_lib


def init_macro_csv():
    print("Loading Macros")
    macro_list_name = address_lib.macros_names
    with open('macro_list.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            macro_place_list_temp = row[1:]
            macro_place_list_temp.insert(0, 0)
            macro_list_name[row[0]] = macro_place_list_temp
            print(row[0])
            print(macro_list_name[row[0]])
