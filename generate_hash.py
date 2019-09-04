__author__ = 'pshubham'
import hashlib
def hash(pas):
    hash_object = hashlib.sha512(pas)
    hex_dig = hash_object.hexdigest()
    return hex_dig

