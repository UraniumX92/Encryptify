from functools import reduce
from datetime import datetime
import numpy as np
import json


def timenow():
    """
    Current timestamp
    :return: float - timestamp
    """
    return datetime.now().timestamp()

def key_mod(key:list) -> list:
    """
    Modifies the given key before using it for encryption/decryption

    :param key:
    :return:
    """
    return [int(format(x,'08b')[::-1],2) for x in key]


def get_key(strval:str) -> list[int]:
    """
    takes string, tries to decode using json, converts to list
    checks if all the elements in the list are integers or not, if not, then tries to convert the characters to integer using ord().
    if it fails to so.. then entire string will be taken as string key, and each character of this string will be converted to integer and returns as list

    :param strval: str
    :return: list[int]
    """
    k = []
    try:
        k = json.loads(strval)
        if type(k) != type(list()):
            raise json.decoder.JSONDecodeError("not int","",0)
        elif any(type(x) != type(int()) for x in k):
            raise json.decoder.JSONDecodeError("not int","",0)
    except json.decoder.JSONDecodeError:
        k = [abs(ord(x))%256 for x in strval]
    return k


def get_compact_key(strval: str) -> str:
    """
    takes a string, converts it into a list of ints using get_key(),
    then converts this list into string with no spaces and removes the square brackets and returns it

    :param strval:
    :return: str
    """
    return str(get_key(strval)).replace(" ", "")

def get_seed(array:list):
    """
    Obtains the seed from given array and returns it.

    :param array : an array from which seed is to be obtained
    :return: int - seed obtained from the key
    """
    max_seed = 4294967296 # This value is 2**32 and maximum value allowed for np.random.seed()
    def seed_func(a,b):
        """
        function to pass in reduce() to get the seed
        """
        if is_even(a) and is_even(b):
            return (2*a)+b
        elif is_even(a) and is_odd(b):
            return (2*b)+a
        elif is_odd(a) and is_even(b):
            return (b+a)//a
        else: # odd , odd
            return (a*b)+(abs(b-a)//a)
    return (reduce(seed_func,array) + (sum(array)//len(array))) % (max_seed)

def scramble(array:np.ndarray,seed):
    """
    Scrambles the array using the given seed

    :param array:
    :param seed:
    :return: scrambled array
    """
    scrambled = array.copy()
    np.random.seed(seed)
    np.random.shuffle(scrambled)
    np.random.seed()
    return scrambled

def unscramble(array:np.ndarray,seed):
    """
    Unscrambles the array using the givnen seed

    :param array:
    :param seed:
    :return: unscrambled array
    """
    scrambled = array.copy()
    temp = np.arange(0,len(array))
    temp = scramble(temp,seed)
    sorted_indices = np.argsort(temp)
    unscrambled = scrambled[sorted_indices]
    return unscrambled

def xor_data(arr:np.ndarray, key:list) -> np.ndarray:
    """
    takes an array and xor encrypts it using key

    :param arr: list
    :param key: list
    :return: list (encrypted rgb values)
    """
    size = len(arr)
    k_len = len(key)
    key = key_mod(key)
    # Repeating key to match the size of the arr list. this method is faster than previous method
    key = (key*((size//k_len)+1))[:size]
    key = np.array(key).astype('uint8')
    arr ^= key # xor'ing each value of arr with key value
    return arr


def is_even(n):
    return n%2==0

def is_odd(n):
    return n%2!=0