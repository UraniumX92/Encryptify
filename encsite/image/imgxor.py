from PIL import Image
import numpy as np
from itertools import chain
import utils


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

def encrypt_image(img:Image.Image,key:str="") -> Image.Image:
    """
    Takes an image and key and encrypts the image using key and returns the encrypted image

    :param img: PIL.Image.Image - Image to be encrypted
    :return: PIL.Image.Image - Encrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width , height = img.size
    img_data = img_to_array(scrambler(img, key))
    xored = xor_img_data(img_data,key)
    nimg = array_to_img(xored, height, width)
    return nimg

def decrypt_image(img:Image.Image,key:str) -> Image.Image:
    """
    Takes the image and key, and decrypts the encrypted image using key and returns the decrypted image

    :param img: image to be decrypted
    :param key: encryption key
    :return: PIL.Image.Image - Decrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width, height = img.size
    img_data = img_to_array(img)
    xored = xor_img_data(img_data, key)
    img2 = array_to_img(xored, height=height, width=width)
    data = img_to_array(unscrambler(img2, key))
    nimg = array_to_img(data, height, width)
    return nimg

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
    nimg = Image.fromarray(scram,"RGB")
    return nimg

def p_unscram(img:Image.Image,key):
    pdata = np.array(img)
    pdata = pdata.reshape((img.height*img.width,3))
    seed = utils.get_seed(key[::-1])
    unscram = utils.unscramble(pdata,seed)
    unscram = unscram.reshape((img.height,img.width,3))
    nimg = Image.fromarray(unscram,"RGB")
    return nimg

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

if __name__ == '__main__':
    key = utils.get_key(input("Enter key: "))
    car = Image.open("car.png")
    fruit = Image.open("fruit.jpg")
    inp = '1'

    t1 = utils.timenow()
    cs = p_scram(car, key)
    t2 = utils.timenow()
    print(f"scram car: {t2-t1}")

    t1 = utils.timenow()
    fs = p_scram(fruit, key)
    t2 = utils.timenow()
    print(f"scram fruit: {t2-t1}")

    t1 = utils.timenow()
    cu = p_unscram(cs, key)
    t2 = utils.timenow()
    print(f"unscram car: {t2-t1}")

    t1 = utils.timenow()
    fu = p_unscram(fs, key)
    t2 = utils.timenow()
    print(f"unscram fruit: {t2-t1}")
    while inp=='1':
        img = input("1.car\n2.fruit\n: ")
        state = input("1.scrambled\n2.unscrambled\n: ")
        match img,state:
            case '1','1':
                cs.show()
            case '1','2':
                cu.show()
            case '2','1':
                fs.show()
            case '2','2':
                fu.show()
            case _:
                pass
        inp = input("1.Continue\n2.Exit\n: ")
        if inp=='1':
            option = input("Enter // for same key, else new key: ")
            if option!='//':
                key = utils.get_key(option)
                if input('1.us car\n2.us fruit\n: ')=='1':
                    p_unscram(cs, key).show()
                else:
                    p_unscram(fs, key).show()
