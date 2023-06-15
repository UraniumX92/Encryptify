def decimal_to_binary(num):
    """
    		:return:  8-bit binary as string if num is in range of 2^8 else the length of string might be higher depending on value.
    """
    negative = num<0
    bnum = format(abs(num),'08b')
    if negative:
        bnum = f"-{bnum}"
    return bnum

def binary_to_decimal(bnum):
    """
    		takes a binary value as a string, converts binary to int and returns int.
    		:return: int converted from given binary
    """
    return int(bnum,2)

def binary_to_text(bin_str:str):
    blist = bin_str.split(" ")
    blist = [x for x in blist if x]
    text = ""
    for bnum in blist:
        text += chr(binary_to_decimal(bnum))
    return text

def text_to_binary(txt:str):
    bstr = ""
    for char in txt:
        bstr += f"{decimal_to_binary(ord(char))} "
    return bstr