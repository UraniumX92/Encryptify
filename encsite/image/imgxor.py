from PIL import Image
from itertools import chain
import utils


def xor_img_data(img_arr:list, key:list) -> list:
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
    key = (key*((size//len(key))+1))[:size]
    for i in range(size):
        img_arr[i] = img_arr[i] ^ key[i]
    return img_arr


def img_to_list(img:Image.Image) -> list:
    """
    Takes an image and returns it's rgb values as list

    :param img: PIL.Image.Image
    :return: list
    """
    return list(chain.from_iterable(img.getdata()))


def list_to_img(img_list:list,height:int,width:int) -> Image.Image:
    """
    takes list of rgb values and creates an image using the values and returns it

    :param img_list : list
    :return: PIL.Image.Image
    """
    return Image.frombytes("RGB", (width,height), bytes(img_list))


def encrypt_image(img:Image.Image,key:str="") -> Image.Image:
    """
    Takes an image and key and encrypts the image using key and returns the encrypted image

    :param img: PIL.Image.Image - Image to be encrypted
    :return: PIL.Image.Image - Encrypted image
    """
    key = utils.get_key(key)
    img = img.convert(mode="RGB") if img.mode != "RGB" else img
    width , height = img.size
    img_data = img_to_list(scrambler(img))
    xored = xor_img_data(img_data,key)
    return list_to_img(xored,height,width)


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
    img_data = img_to_list(img)
    xored = xor_img_data(img_data, key)
    img2 = list_to_img(xored, height=height, width=width)
    data = img_to_list(unscrambler(img2))
    return list_to_img(data, height, width)


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


def scrambler(img) -> Image.Image:
    """
    Takes an image and scrambles it and returns the scrambled image
    (this function is inverse of unscrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    data = img_to_list(img)
    data = utils.split_and_flip(data)
    newimg = list_to_img(data, height=h, width=w)
    newimg = newimg.rotate(90, expand=1)
    data = utils.split_and_flip(img_to_list(newimg))
    return list_to_img(data, width=h, height=w).rotate(-90,expand=1)


def unscrambler(img) -> Image.Image:
    """
    Takes an image and performs inverse of scrambling algorithm
    i.e unscrambles the scrambled image and returns it
    (this function is inverse of scrambler(img) function)
    :param img:
    :return: PIL.Image.Image
    """
    w,h = img.size
    img = img.rotate(90,expand=1)
    data = utils.split_and_flip(img_to_list(img))
    newimg = list_to_img(data, w, h).rotate(-90, expand=1)
    data = utils.split_and_flip(img_to_list(newimg))
    return list_to_img(data, h, w)

# todo: give estimated time of encryption/decryption for a given image
#   use this formula for calculation
#   x = (avg * (w*h)) / (1920*1080)
#   here,
#   x = Estimated time to encrypt/decrypt the image,
#   avg = Average time taken to encrypt/decrypt the blue car image of size 1920x1080,
#   w,h = width , height of given image.
#   Note: x gives the maximum possible time. NEEDS ACCURACY IMPROVEMENT for largeer images.
#   and... I think we are good to go for the website development now.

if __name__ == '__main__':
    pass