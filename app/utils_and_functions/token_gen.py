from random import choice

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_token(n):
    return "".join([choice(alphabet) for i in range(n)])
