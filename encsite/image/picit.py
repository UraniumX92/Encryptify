from PIL import Image
import numpy as np
import utils


DEFAULT_COLOR = (0, 0, 0)
MAX_PIXEL_LIMIT = 2360
MAX_TEXT_LIMIT = (2 ** 24) - 1
# signature text should not contain any spaces.
SIGNATURE_TEXT = utils.envs["PICIT_SIGNATURE_TEXT"]
sgt_list = utils.json.loads(utils.envs["PICIT_SIGNATURE_LIST"])
sgt_list.append(SIGNATURE_TEXT)


def hide_data(message: str, key: list, enc_strictnes: tuple) -> Image.Image:
    """
    takes message and key, encrypts the message and stores it in Image, returns the Image object

    :param message: string of message
    :param key: encryption key (list of int)
    :param enc_strictnes: strictness of encryption, a tuple of length 3
    :return: Image which is having data hidden in it
    :raises OverflowError : if the image requires more than 2360x2360 pixels
    """
    # Adding signature text to detect the key while extracting the data from image
    message = f"{SIGNATURE_TEXT} {message} {SIGNATURE_TEXT}"
    orientation = utils.randint(0, 1)
    required_pixels = 6
    tup_size = 3
    key_tup = utils.oneD_to_2DList(key, tup_size, tuple)
    encrypted_text = utils.ciph(message, key)
    enc_tup = [ord(x) for x in encrypted_text]
    enc_tup = utils.oneD_to_2DList(enc_tup, tup_size, tuple)
    required_pixels += (len(enc_tup) + len(key_tup))
    img_len = utils.get_dimension(required_pixels)
    if img_len > MAX_PIXEL_LIMIT or len(encrypted_text) > MAX_TEXT_LIMIT:
        raise OverflowError(
            "Image size too big, divide the size of text into smaller chunks and try to create multiple images.")
    # img len to use as index, for ease of use, decrementing by 1 and storing in variable below
    ti_len = img_len - 1
    map_to_pixel = {
        'txtlen': (0, 0),
        'txtco-ord': (0, ti_len),
        'keylen': (ti_len, 0),
        'keyco-ord': (ti_len, ti_len),
        'encstrict': ((0, 1), (1, 0))
    }
    # pixels which are storing meta data should be ignored while writing data in image
    ignored_pixels = [(0, 0), (0, ti_len), (ti_len, 0), (ti_len, ti_len), (1, 0), (0, 1)]
    # creating a new Image and putting encryption strictness pixels
    img = Image.new("RGB", (img_len, img_len), DEFAULT_COLOR)
    img.putpixel(map_to_pixel['encstrict'][0], enc_strictnes)
    img.putpixel(map_to_pixel['encstrict'][1], enc_strictnes)

    # ---------- creating tuples ---------- #

    # --------- Text tuples --------- #
    # text length tuple
    tltup = utils.get_tuple_from_size(len(encrypted_text))
    img.putpixel(map_to_pixel['txtlen'], tltup)

    # --------- Key tuples --------- #
    # key length tuple
    kltup = utils.get_tuple_from_size(len(key))
    img.putpixel(map_to_pixel['keylen'], kltup)

    # putting encryption key pixels
    kctup = (0, orientation, 0)
    i, j = 0, 0
    count = 0
    i1, j1 = 0, 0
    if enc_strictnes[0] == 0:
        # key is auto generated , include the key in image
        index = 0
        while (i < img_len or j < img_len) and index != len(key_tup):
            j = 0
            while j < img_len and index != len(key_tup):
                t = key_tup[index]
                if len(t) < 3:
                    t = list(t)
                    while len(t) != 3:
                        t.append(0)
                    t = tuple(t)
                if orientation == 0:
                    pxl = (i, j)
                    if pxl in ignored_pixels:
                        pass
                    else:
                        if count == 0:
                            kctup = (i, orientation, j)
                            count += 1
                        img.putpixel(pxl, t)
                        i1, j1 = i, j
                        ignored_pixels.append(pxl)
                        index += 1
                else:
                    pxl = (j, i)
                    if pxl in ignored_pixels:
                        pass
                    else:
                        if count == 0:
                            kctup = (j, orientation, i)
                            count += 1
                        img.putpixel(pxl, t)
                        i1, j1 = i, j
                        ignored_pixels.append(pxl)
                        index += 1
                j += 1
            i += 1

        # putting the initial key co-ordinates in (n,n)
        img.putpixel(map_to_pixel['keyco-ord'], kctup)
        i -= 1
        j -= 1
    else:
        # putting the initial key co-ordinates in (n,n)
        kctup = (0, orientation, 0)
        img.putpixel(map_to_pixel['keyco-ord'], kctup)

    # putting encrypted text pixels
    tctup = (0, 0, 0)
    count = 0
    index = 0
    i, j = i1, j1
    while (i < img_len or j < img_len) and index != len(enc_tup):
        # not changing the value of j initially, so that the text co-ordinates are not modified
        if count != 0:
            j = 0

        while j < img_len and index != len(enc_tup):
            t = enc_tup[index]
            if len(t) < 3:
                t = list(t)
                while len(t) != 3:
                    t.append(0)
                t = tuple(t)
            if orientation == 0:
                pxl = (i, j)
                if pxl in ignored_pixels:
                    pass
                else:
                    if count == 0:
                        tctup = (i, utils.randint(0, 255), j)
                        count += 1
                    img.putpixel(pxl, t)
                    index += 1
            else:
                pxl = (j, i)
                if pxl in ignored_pixels:
                    pass
                else:
                    if count == 0:
                        tctup = (j, utils.randint(0, 255), i)
                        count += 1
                    img.putpixel(pxl, t)
                    index += 1
            j += 1
        i += 1
    # putting the initial co-ordinates of text in (0,n)
    img.putpixel(map_to_pixel['txtco-ord'], tctup)
    img = scrambler(img,key)
    return img


def check_img(img: Image.Image,key:list) -> Image.Image:
    """
    Takes an Image object and checks if the given image is encoded using PicIt or not
    if image is not encoded by PicIt, then raises the exception `TypeError`
    or else returns None

    :param img: takes an PIL.Image.Image object
    :return: Image , rotated image with right orientation if image is not oriented
    :raises TypeError if the given image `img` is not encoded by PicIt tool
    """
    img_len, x = img.size
    # checking if the image is square or not (i.e length should be equal to width)
    if x != img_len:
        raise TypeError(f"Given image is not encoded by PicIt, code 1")
    # img len to use as index, for ease of use, decrementing by 1 and storing in variable below
    ti_len = img_len - 1
    map_to_pixel = {
        'txtlen': (0, 0),
        'txtco-ord': (0, ti_len),
        'keylen': (ti_len, 0),
        'keyco-ord': (ti_len, ti_len),
        'encstrict': ((0, 1), (1, 0))
    }
    # checking if the encryption strictness tuples are present in image or not,
    # there is chance that image can be rotated sometimes, so we also check by rotating the image

    img = unscrambler(img,key)
    p01, p10 = img.getpixel(map_to_pixel['encstrict'][0]), img.getpixel(map_to_pixel['encstrict'][1])
    for i in range(3):
        if p01 != p10:
            img = scrambler(img,key)
            img = img.rotate(angle=90)
            img = unscrambler(img,key)
            p01, p10 = img.getpixel(map_to_pixel['encstrict'][0]), img.getpixel(map_to_pixel['encstrict'][1])
        else:
            break
    if p01 != p10:
        raise TypeError("Given image is not encoded by PicIt, code 2")

    # check if the middle value of key co-ordinate pixel is either 0 or 1 (this value represents the orientation of traversal)
    kct = img.getpixel(map_to_pixel['keyco-ord'])
    if kct[1] not in [0, 1]:
        raise TypeError(f"Given image is not encoded by PicIt, code 3 {kct}")
    return img


def extract_data(img: Image.Image) -> str:
    """
        Takes the Image object and extracts the encrypted data from it, returns str: extracted text

        :param img: Image object to extract data from
        :return: str : extracted text
        :raises TypeError : if the given image `img` is not encoded by PicIt tool
    """
    # -- checking if the given image is encoded using PicIt or not -- #
    img = check_img(img)

    # we are here only if Image is encoded using PicIt. safe to extract data and interpret
    img_len = img.size[0]
    ti_len = img_len - 1
    map_to_pixel = {
        'txtlen': (0, 0),
        'txtco-ord': (0, ti_len),
        'keylen': (ti_len, 0),
        'keyco-ord': (ti_len, ti_len),
        'encstrict': ((0, 1), (1, 0))
    }
    # pixels which are storing meta data should be ignored while writing data in image
    ignored_pixels = [(0, 0), (0, ti_len), (ti_len, 0), (ti_len, ti_len), (1, 0), (0, 1)]
    # extracting metadata
    tltup = img.getpixel(map_to_pixel['txtlen'])
    tctup = img.getpixel(map_to_pixel['txtco-ord'])
    kltup = img.getpixel(map_to_pixel['keylen'])
    kctup = img.getpixel(map_to_pixel['keyco-ord'])
    encstrict = img.getpixel(map_to_pixel['encstrict'][0])

    orientation = kctup[1]
    text_length = utils.get_size_from_tuple(tltup)
    key = []
    text_list = []
    txtuplen = int(text_length / 3) + 1

    i, j = 0, 0
    if encstrict[0] == 0:
        # key is auto generated. extract key from image and send the decrypted data
        key_length = utils.get_size_from_tuple(kltup)
        ktuplen = int(key_length / 3) + 1
        temp_kl = ktuplen
        i, orientation, j = kctup
        if orientation == 1:
            i, j = j, i

        # extracting the key
        while (i < img_len or j < img_len) and temp_kl != 0:
            j = 0
            while j < img_len and temp_kl != 0:
                if orientation == 0:
                    pxl = (i, j)
                    if pxl in ignored_pixels:
                        pass
                    else:
                        t = img.getpixel(pxl)
                        temp_kl -= 1
                        for v in t:
                            key.append(v)
                else:
                    pxl = (j, i)
                    if pxl in ignored_pixels:
                        pass
                    else:
                        t = img.getpixel(pxl)
                        temp_kl -= 1
                        for v in t:
                            key.append(v)
                j += 1
            i += 1

    # if key is manually added, then only raw text data will be returned
    temp_tl = txtuplen
    i, _x, j = tctup
    if orientation == 1:
        i, j = j, i
    count = 0
    break_flag = False
    while (i < img_len or j < img_len) and temp_tl != 0:
        # not changing the value of j initially, so that the text extraction operation co-ordinates are not modified
        if count != 0:
            j = 0
        else:
            count += 1
        while j < img_len and temp_tl != 0:
            if orientation == 0:
                pxl = (i, j)
                if pxl in ignored_pixels:
                    pass
                else:
                    t = img.getpixel(pxl)
                    if t == DEFAULT_COLOR:
                        break_flag = True
                        break
                    else:
                        temp_tl -= 1
                        for v in t:
                            text_list.append(v)
            else:
                pxl = (j, i)
                if pxl in ignored_pixels:
                    pass
                else:
                    t = img.getpixel(pxl)
                    if t == DEFAULT_COLOR:
                        break_flag = True
                        break
                    else:
                        temp_tl -= 1
                        for v in t:
                            text_list.append(v)
            j += 1
        if break_flag:
            break
        else:
            i += 1
    # slicing the text and key to their expected lengths
    text_list = text_list[:text_length]
    if len(key) > 0:
        key = key[:key_length]
        text = "".join([chr(x) for x in text_list])
        return utils.deciph(text, key)
    else:
        return "".join([chr(x) for x in text_list])


def get_enc_tup(img: Image.Image) -> tuple:
    """
    takes Image object and returns the encryption strictness tuple
    :param img:
    :return: tuple present at encryption strictness pixel i.e (1,0) or (0,1)
    """
    img = check_img(img)
    return img.getpixel((1, 0))

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

legend = \
"""
    Basic structure and legend:

    (0,0) --> length of text
    (0,n) --> Initial co-ordinates of text
    (n,0) --> length of key
    (n,n) --> Initial co-ordinates of key
    (0,1) and (1,0) --> strictness of encryption
    total: 6
    middle element of key co-ordinates pixel decides if encoding is horizontal or vertical
    0 - vertical
    1 - horizontal
"""