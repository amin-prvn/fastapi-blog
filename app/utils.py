import random
import string
import os

def dir_check_create():
    directory = os.path.dirname(__file__)
    if not os.path.isdir(os.path.join(directory, '../media')):
        os.makedirs(os.path.join(directory, '../media'))
    return directory

def random_string(size: int):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
