import argparse
import random
import string


def calculate_port(message):
    data = message[message.find("(") + 1:message.find(")")]
    split_data = data.split(',')
    return int(split_data[4]) * 256 + int(split_data[5])


def get_random_string():
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(8))


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def extract_status_code(message):
    try:
        return int(message[0:3])
    except:
        return 999
