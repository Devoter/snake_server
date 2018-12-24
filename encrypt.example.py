from hashlib import sha256


def encrypt(name, score):
    return sha256((name + str(score)).encode('utf-8'))
