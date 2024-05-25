import string
import random

CHARACTERS = string.ascii_letters + string.digits + string.punctuation

def generate_password(length, characters=CHARACTERS):
    password = ''.join(random.choice(characters) for i in range(length))
    return password