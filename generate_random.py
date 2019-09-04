import string,random
def generate_random():

    s=string.lowercase+string.digits+string.uppercase
    s = ''.join(random.sample(s,10))
    return s