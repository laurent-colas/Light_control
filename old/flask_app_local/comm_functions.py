import time
import constant



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


def send_address(bus, address, target_pins, state):
    for i in range(len(target_pins)):
        command = "%s %d" % (target_pins[i], state)
        data_list = list(string_to_bytes(command))
        for j in data_list:
            write_number(bus, address, j)
            time.sleep(constant.SLEEP_TIME_I2C)
        time.sleep(0.5)


def send_address_relay_clean(bus, address, command):
    print("Sending command to relay: " + command)
    data_list = list(string_to_bytes(command))
    for j in data_list:
        write_number(bus, address, j)
        time.sleep(constant.SLEEP_TIME_I2C)
    time.sleep(0.1)


def simulate_send_address_brightness(target_pins, brightness):
    for targetPin in target_pins:
        if targetPin > constant.NUM_PWM:
            print(create_relay_string(targetPin, brightness))
            # print('Relay activation' + str(targetPin) + str(brightness))
        else:
            print(str(targetPin) + ' ' + str(brightness))


def send_mixed_address_brightness(bus, address, pwm, target_pins, brightness):
    for targetPin in target_pins:
        if targetPin > constant.NUM_PWM:
            command = create_relay_string(targetPin, brightness)
            # A01 1
            print(command)
            send_address_relay_clean(bus, address, command)
        else:
            print(str(targetPin) + ' ' + str(brightness))
            send_address_brightness(pwm, targetPin, brightness)


def create_relay_string(relay_num, state):
    correct_relay_num = relay_num - constant.NUM_PWM
    if correct_relay_num < 10:
        str_correct_relay_num = str(0) + str(correct_relay_num)
    else:
        str_correct_relay_num = str(correct_relay_num)
    if state >= 1:
        state = 1
    else:
        state = 0
    command = 'A' + str_correct_relay_num + ' ' + str(state)
    return command


def send_address_brightness(pwm, target_pin, brightness):
    pwm_brightness_off = (brightness / 100) * 4096
    print(str(target_pin) + ' ' + str(brightness))
    pwm.set_pwm(target_pin, 0, pwm_brightness_off)
