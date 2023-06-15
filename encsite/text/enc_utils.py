import numpy as np
from . import utils

def generate_ascii_values():
    return [chr(num) for num in range(1, 256)]

# ----------------------------------- #
ascii_values = generate_ascii_values()
ascii_len = len(ascii_values)
# ----------------------------------- #
utils.is_odd(2)

def xor_text(text,key):
    """
    Takes text and xor's it based on key

    :param text:
    :param key:
    :return:
    """
    arr = np.array([ord(x) for x in text])
    key = utils.key_mod(key)
    xored = utils.xor_data(arr,key)
    xored = [chr(x) for x in xored]
    xored_txt = "".join(xored)
    return xored_txt

def scrambler(text,key):
    """
    Takes text and key and scrambles the text based on key

    :param text:
    :param key:
    :return:
    """
    arr = np.array([ord(x) for x in text])
    seed = utils.get_seed(key)
    scram = utils.scramble(arr,seed)
    scram = [chr(x) for x in scram]
    scram_txt = "".join(scram)
    return scram_txt

def unscramber(text,key):
    """
    Takes text and key and unscrambles the text based on key

    :param text:
    :param key:
    :return:
    """
    arr = np.array([ord(x) for x in text])
    seed = utils.get_seed(key)
    unscram = utils.unscramble(arr,seed)
    unscram = [chr(x) for x in unscram]
    unscram_txt = "".join(unscram)
    return unscram_txt

def ciph(text: str, key: list) -> str:
    """
    Takes text and key, encrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : encrypted text
    """
    ciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) + key[i]
        if ascii_index >= ascii_len:
            ascii_index = ascii_index % ascii_len
        elif ascii_index < 0:
            ascii_index = ascii_len - ((ascii_index * -1)%ascii_len)
        ciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return ciphered_text


def deciph(text: str, key: list) -> str:
    """
    Takes text and key, decrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : decrypted text
    """
    deciphered_text = ''
    i = 0
    for charx in text:
        ascii_index = ord(charx) - key[i]
        if ascii_index >= ascii_len:
            ascii_index = ascii_index % ascii_len
        elif ascii_index < 0:
            ascii_index = ascii_len - ((ascii_index * -1)%ascii_len)
        deciphered_text += ascii_values[ascii_index - 1]
        i += 1
        if i == len(key):
            i = 0
    return deciphered_text

# text = "Hello this is the xor text which is not working fine"
# keyx = utils.get_key("xorkey")
# x = xor_text(text,keyx)
# print("xored",x)
# xn = xor_text(x,keyx)
# print("unxored",xn)
# print(xn==text)

if __name__ == '__main__':
    text = input("Enter text: ")
    key = input("Enter key: ")
    key = utils.get_key(key)
    op = input("1. Enc\n2. Dec\nselect: ")
    if op=='1':
        op = input("1.Vigenere\n2.XOR\n3.Scramble\nselect: ")
        match op:
            case '1':
                print(ciph(text,key))
            case '2':
                x = xor_text(text,key)
                print(x)
                print([ord(a) for a in x])
                print(xor_text(x,key))
            case '3':
                print(scrambler(text,key))
    else:
        op = input("1.Vigenere\n2.XOR\n3.Scramble\nselect: ")
        match op:
            case '1':
                print(deciph(text, key))
            case '2':
                print(xor_text(text,key))
            case '3':
                print(unscramber(text,key))
