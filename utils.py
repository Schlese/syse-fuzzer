import random
import string

def calculate_port(message):
    data = message[message.find("(") + 1:message.find(")")]
    split_data = data.split(',')
    return int(split_data[4]) * 256 + int(split_data[5])


def get_random_string():
    # With combination of lower and upper case
    return ''.join(random.choice(string.ascii_letters) for i in range(8))
