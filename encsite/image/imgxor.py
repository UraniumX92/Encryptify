from PIL import Image
from itertools import chain
import threading
import numpy as np
from . import utils
import os

def xor_img_data(img_arr:np.ndarray, key:list) -> list:
    """
    takes list of rgb values of image and encrypts it using key

    :param img_arr: list
    :param key: list
    :return: list (encrypted rgb values)
    """
    size = len(img_arr)
    k_len = len(key)
    key = utils.key_mod(key)
    # Repeating key to match the size of the img_array list. this method is faster than previous method
    key = (key*((size//k_len)+1))[:size]
    key = np.array(key).astype('uint8')
    img_arr ^= key # xor'ing each value of img_arr with key value
    return img_arr

def img_to_array(img:Image.Image):
    """
    Takes an image and returns it's rgb values as array

    :param img: PIL.Image.Image
    :return: np.ndarray
    """
    return np.array(img).flatten()

def array_to_img(imgarr:np.ndarray, height:int, width:int):
    """
    Takes array of rgb values and creates an image using the values and returns it

    :param img_list : np.ndarray
    :return: PIL.Image.Image
    """
    return Image.fromarray(imgarr.reshape((height, width, 3)), "RGB")

def encrypt_image(img:Image.Image,key:str,thread_cb_list:list['function'],cb_args:list[list]) -> Image.Image:
    """
    Takes an image and key and encrypts the image using key and returns the encrypted image

    :param img: PIL.Image.Image - Image to be encrypted
    :param key: encryption key
    :param thread_cb_list: list of callback functions (exactly 2 functions should be passed in this list)
    :param cb_args: list of list where inner list contains params to pass in callbacks
    :return: PIL.Image.Image - Encrypted image
    """
    cb1, cb2 = thread_cb_list
    args1, args2 = cb_args
    th1 = threading.Thread(target=cb1, args=args1)
    th2 = threading.Thread(target=cb2, args=args2)
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width , height = img.size
    th1.start()
    img_data = img_to_array(scrambler(img, key))
    xored = xor_img_data(img_data,key)
    nimg = array_to_img(xored, height, width)
    th2.start()
    th2.join()
    return nimg

def decrypt_image(img:Image.Image,key:str,thread_cb_list:list['function'],cb_args:list[list]) -> Image.Image:
    """
    Takes the image and key, and decrypts the encrypted image using key and returns the decrypted image

    :param img: image to be decrypted
    :param key: encryption key
    :param thread_cb_list: list of callback functions (exactly 2 functions should be passed in this list)
    :param cb_args: list of list where inner list contains params to pass in callbacks
    :return: PIL.Image.Image - Decrypted image
    """
    cb1,cb2 = thread_cb_list
    args1,args2 = cb_args
    th1 = threading.Thread(target=cb1,args=args1)
    th2 = threading.Thread(target=cb2,args=args2)
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width, height = img.size
    th1.start()
    img_data = img_to_array(img)
    xored = xor_img_data(img_data, key)
    img2 = array_to_img(xored, height=height, width=width)
    data = img_to_array(unscrambler(img2, key))
    nimg = array_to_img(data, height, width)
    th2.start()
    th2.join()
    return nimg

def save_after(action:'function',thr_to_join:threading.Thread,action_args:list,job,spath:str,tmpath:str):
    """

    :param action:
    :param action_args:
    :return:
    """
    thr_to_join.join()
    print(os.getcwd())
    img = Image.open(tmpath)
    action_args.insert(0,img)
    rimg:Image.Image = action(*action_args)
    rimg.save(spath,format="PNG")
    job.result_saved = True
    job.save()
    os.remove(tmpath)


def resizer(img:Image.Image,max_size:int) -> Image.Image:
    """
    Takes the image and resizes it according the max_size provided while keeping the aspect ratio same as original image.

    :param img: PIL.Image.Image
    :param max_size: int
    :return: PIL.Image.Image - Resized image
    """
    width,height = img.size
    multiplier = max_size/max(width,height)
    new_size = int(multiplier*width),int(multiplier*height)
    return img.resize(new_size)

def scrambler(img,key) -> Image.Image:
    """
    Takes an image and scrambles it and returns the scrambled image
    (this function is inverse of unscrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_array(img)
    seed = utils.get_seed(key[::-1])
    data = utils.scramble(data,seed)
    return array_to_img(data, height=h, width=w)


def unscrambler(img,key) -> Image.Image:
    """
    Takes an image and performs inverse of scrambling algorithm
    i.e unscrambles the scrambled image and returns it
    (this function is inverse of scrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_array(img)
    seed = utils.get_seed(key[::-1])
    data = utils.unscramble(data, seed)
    return array_to_img(data, h, w)

def p_scram(img:Image.Image,key):
    pdata = np.array(img)
    pdata = pdata.reshape((img.height*img.width,3))
    seed = utils.get_seed(key[::-1])
    scram = utils.scramble(pdata,seed)
    scram = scram.reshape((img.height,img.width,3))
    return Image.fromarray(scram,"RGB")


def p_unscram(img:Image.Image,key):
    pdata = np.array(img)
    pdata = pdata.reshape((img.height*img.width,3))
    seed = utils.get_seed(key[::-1])
    unscram = utils.unscramble(pdata,seed)
    unscram = unscram.reshape((img.height,img.width,3))
    return Image.fromarray(unscram,"RGB")


# def pixel_scrambler(img,key):
#     hscram = p_scram(img, key)
#     hscram = hscram.rotate(90,expand=True)
#     vscram = p_scram(hscram, key)
#     vscram = vscram.rotate(-90,expand=True)
#     return vscram
#
# def pixel_unscrambler(img,key):
#     nimg = img.rotate(90,expand=True)
#     vuscram = p_unscram(nimg, key)
#     vuscram = vuscram.rotate(-90, expand=True)
#     huscram = p_unscram(vuscram, key)
#     return huscram