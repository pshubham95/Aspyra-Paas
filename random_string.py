__author__ = 'Shubham'
import string
import random
def id_generator(size=20, chars=string.ascii_uppercase + string.digits+string.lowercase):
    return ''.join(random.choice(chars) for _ in range(size))
