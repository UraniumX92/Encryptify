from django.core.files.uploadedfile import \
    InMemoryUploadedFile,\
    SimpleUploadedFile,\
    TemporaryUploadedFile
from django.utils import timezone
from datetime import datetime
from functools import reduce
import threading
import numpy as np
import math
import random
import json
import os
from . import binary_utils
from dotenv import load_dotenv
load_dotenv()
envs = os.environ
bullet_char = "\u2022"


def generate_ascii_values():
    return [chr(num) for num in range(1, 256)]

# ----------------------------------- #
ascii_values = generate_ascii_values()
ascii_len = len(ascii_values)
# ----------------------------------- #

def randint(start,end):
    return random.randint(start,end)

def timenow(ts=True):
    """
    Current timestamp
    :return: float - timestamp
    """
    t = datetime.now(tz=timezone.utc)
    return t.timestamp() if ts else t

def read_bytes(filename,encoding='utf-16'):
    with open(filename,'rb') as f:
        return f.read().decode(encoding)

def write_bytes(filename,data,encoding='utf-16'):
    with open(filename,'wb') as f:
        f.write(data.encode(encoding))

def add_time_ts(ts,days=0):
    """
    Adds time to given ts and returns the resultant timestamp

    :param ts:
    :param days:
    :param hours:
    :param minutes:
    :return: int
    """
    minute = 60
    hour = minute*60
    day = hour * 24
    return (ts + (days*day))

def random_KeyGen(keylen: int) -> list[int]:
    return random.sample(range(256), keylen, counts=[2 for x in range(256)])


def to_even(n):
    """
    Takes an int n, if n is odd integer then converts n to an even number and returns n, else returns n as it is.

    :param n: int
    :return: int : closest even number to n in range(0,255)
    """
    if n%2==0:
        return n
    else:
        return n-1


def to_odd(n):
    """
    Takes an int n, if n is even integer then converts n to an odd number and returns n. else returns n as it is.

    :param n: int
    :return: int : closest odd number to n in range(0,255)
    """
    if n%2!=0:
        return n
    else:
        return n+1


def ciph(text: str, key: list) -> str:
    """
    Takes text and key, encrypts the text based on key provided and returns it

    :param text:
    :param key:
    :return: str : encrypted text
    """
    text = txt_scrambler(text,key)
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
    deciphered_text = txt_unscramber(deciphered_text,key)
    return deciphered_text

def txt_scrambler(text,key):
    """
    Takes text and key and scrambles the text based on key

    :param text:
    :param key:
    :return:
    """
    arr = np.array([ord(x) for x in text])
    seed = get_seed(key)
    scram = scramble(arr,seed)
    scram = [chr(x) for x in scram]
    scram_txt = "".join(scram)
    return scram_txt

def txt_unscramber(text,key):
    """
    Takes text and key and unscrambles the text based on key

    :param text:
    :param key:
    :return:
    """
    arr = np.array([ord(x) for x in text])
    seed = get_seed(key)
    unscram = unscramble(arr,seed)
    unscram = [chr(x) for x in unscram]
    unscram_txt = "".join(unscram)
    return unscram_txt

def memory_to_simple_file(mfile):
    if isinstance(mfile,TemporaryUploadedFile):
        mfile.file.close_called = True
    elif isinstance(mfile,InMemoryUploadedFile):
        mfile = SimpleUploadedFile(mfile.name,mfile.read(),mfile.content_type)
    return mfile


def dump_json(object, filename):
    with open(filename, "w") as dump:
        json.dump(object, dump, indent=4)


def load_json(filename):
    with open(filename, "r") as load:
        return json.load(load)


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


def get_compact_key(strval: str,strip=False) -> str:
    """
    takes a string, converts it into a list of ints using get_key(),
    then converts this list into string with no spaces and removes the square brackets and returns it

    :param strval:
    :return: str
    """
    return str(get_key(strval)).replace(" ", "")


def circular_increment(value: int, limit: int):
    """
    Does a circular increment to the given number and returns the incremented number.
    :param value: int
    :param limit: int
    :return: int - circularly incremented value
    """
    value += 1
    if value >= limit:
        value = 0
    return value


def split_and_flip(array:list):
    """
    divides the list into 2 halves and flips each half, joins the flipped halves and returns single list
    does the same thing with each half recursively if the list contains even number of items/
    because array with odd number items cannot be split and obtained back in original form. where as array with even number items
    can be split recursively and can be obtained as original form of array.

    :param array: list
    :return: list - modified
    """
    size = len(array)
    halfsize_int = size // 2
    h1 = array[:halfsize_int]
    h2 = array[halfsize_int:]
    s1 = halfsize_int
    s2 = size - halfsize_int
    # first half
    if s1%2==0:
        h1 = split_and_flip(h1)
    # second half
    if s2%2==0:
        h2 = split_and_flip(h2)
    return h1[::-1] + h2[::-1]

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

def is_even(n):
    return n%2==0

def is_odd(n):
    return n%2!=0

def scramble(data:np.ndarray,seed:int):
    """
    Scrambles the data, using a seed and returns it.

    :param data: data to be scrambled
    :param seed: seed to be used for rng
    :return: modified data
    """
    scrambled = data.copy()
    np.random.seed(seed)
    np.random.shuffle(scrambled)
    # Resetting the seed to default (to avoid problems using random elsewhere)
    np.random.seed()
    return scrambled

def unscramble(scrambled:np.ndarray,seed:int):
    """
    Unscrambles the scrambled data using a seed and returns it.

    :param scrambled: scrambled data
    :param seed: seed to be used for rng
    :return: modified data
    """
    temp = np.arange(len(scrambled))
    s_temp = scramble(temp, seed)
    sorted_indices = np.argsort(s_temp)
    return scrambled[sorted_indices]

def change(key):
    """
    Temp function to use for testing.
    this function changes each value of a given list of integers by +/- 1
    :param key:
    :return:
    """
    key = json.loads(key)
    kl = len(key)
    for i in range(kl):
        value = key[i]
        if value == 255:
            key[i] = 254
        elif value == 0:
            key[i] = 1
        else:
            r = random.randint(0, 10)
            if r % 2 == 0:
                key[i] = value + 1
            else:
                key[i] = value - 1
    return key


def oneD_to_2DList(list1D:list,size:int,func=None) -> list:
    """
    Takes a 1-D list and converts it into 2-D list where `size` is the size of each list in 2nd dimension

    :param list1D: One dimenstional list
    :param size: size of each list in 2nd dimension
    :param func: (Optional) Function to execute on each list in 2nd dimension
    :return: 2-D List
    """
    if not func :
        def f(a):
            return a
        func = f

    return [func(list1D[i:i+size]) for i in range(0,len(list1D),size)]


def get_dimension(num):
    """
    This is to use to get the dimension for image size, suppose if `num` pixels are required to store the metadata + data
    then this function gives the minimum dimension required for a square image.

    :param num: number of pixels required
    :return: int: minimum dimension required for a square image. which on squaring is just greater than given `num`

    """
    return math.ceil(num**(1/2))


def get_exponent(num,base=2):
    """
    takes a number and base
    returns a smallest int x , such that base ** x > num

    :param num: integer number
    :param base: base for the exponent (default value is 2)
    :return: smallest int x, such that base ** x > num
    """
    return math.ceil(math.log(num,base))


def get_tuple_from_size(num:int) -> tuple:
    """
    takes a number `num` and creates it's 24-bit binary, then slices the 24-bit into three 8-bit binaries
    converts these 3 binaries to int and returns the tuple of size 3

    :param num: integer number
    :return: tuple which represents the `num` in binary when all 3 elements of tuple are concatenated
    """
    bnum = binary_utils.decimal_to_binary(num)
    bnum = f"{'0'*(24-len(bnum))}{bnum}"
    btup = [bnum[i:8+i] for i in range(0,len(bnum),8)]
    return tuple([binary_utils.binary_to_decimal(x) for x in btup])


def get_size_from_tuple(tup:tuple) -> int:
    """
    takes the tuple of size 3 and converts each int element of tuple to 8-bit binaries, concatenates these three binaries to get 24-bit binary
    converts this 24-bit binary to integer and returns it

    :param tup: tuple of size 3, containing integers
    :return: int : which is represented by the tuple when all elements are converted to 8-bit binaries and concatenated to get 24-bit binary and then converted to an integer
    """
    btup = [binary_utils.decimal_to_binary(x) for x in tup]
    b24bit = "".join(btup)
    return binary_utils.binary_to_decimal(b24bit)

def set_path_extension(path,ext):
    plist = path.split('.')
    plist[-1] = ext
    return '.'.join(plist)

def cb_start_job_time(job):
    job.started_at = timenow(ts=False)
    job.save()

def cb_finish_job_time(job,expiry_days=None,protected_dict:dict=None):
    tnow = timenow(ts=False)
    job.finished_at = tnow
    if expiry_days:
        job.expires_at = datetime.fromtimestamp(add_time_ts(tnow.timestamp(),days=expiry_days),tz=timezone.utc)
    if protected_dict:
        job.protected = protected_dict['protected']
    job.save()

def steg_helper_thread_enc(img,text:str,pdict):
    ipath = pdict["img"]
    img.save(ipath,"PNG")
    tpath = pdict["txt"]
    write_bytes(tpath,text)

def steg_helper_thread_dec(img,path):
    img.save(path,"PNG")

def picit_helper_thread_enc(text,path):
    write_bytes(path,text)

def picit_helper_thread_dec(img,path,job,expiry_days):
    tnow = timenow(ts=False)
    img.save(path,"PNG")
    job.expires_at = datetime.fromtimestamp(add_time_ts(tnow.timestamp(), days=expiry_days), tz=timezone.utc)


if __name__ == '__main__':
    arr = [x for x in range(38024)]
    old = split_and_flip(arr, 0)
    new = split_and_flip(arr)
    # print(old)
    # print(new)
    reset = split_and_flip(new)
    print(sorted(new) == reset)