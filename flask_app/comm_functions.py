import time


def write_number(bus, address, value):
    bus.write_byte(address, value)
    # bus.write_byte(address_2, value)
    # bus.write_byte_data(address, 0, value)
    return -1


def read_number(bus, address):
    # number = bus.read_byte(address)
    number = bus.read_byte_data(address, 1)
    return number


def string_to_bytes(val):
    ret_val = []
    for c in val:
        ret_val.append(ord(c))
    return ret_val


def send_address(bus, address, targetPins, state):
    for i in range(len(targetPins)):
        command = "%s %d" % (targetPins[i], state)
        data_list = list(string_to_bytes(command))
        for j in data_list:
            write_number(bus, address, j)
            time.sleep(.1)
        time.sleep(0.5)


def simulate_send_address(targetPins, state):
    for i in range(len(targetPins)):
        print(targetPins[i])
        print(state)