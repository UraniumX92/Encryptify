from datetime import datetime


bullet_char = "\u2022"
# ----------------------------------- #

def timenow():
    """
    Current timestamp
    :return: float - timestamp
    """
    return datetime.now().timestamp()

def create_uid(hash):
    """
    Creates a UID, by adding timestamp in the given hash.
    :param hash:
    :return: str : UID
    """
    hlen = len(hash)
    ts = str(timenow()).split('.')[0]
    ti = 0
    hi = 0
    uid = ''
    for i in range(len(ts)*2):
        if i%2==0:
            uid += hash[hi]
            hi +=1
        else:
            uid += ts[ti]
            ti += 1

    while hi!=hlen:
        uid += hash[hi]
        hi += 1
    return uid

import time
def test_task(*args,**kwargs):
    while True:
        for i in range(100):
            print(i)
        time.sleep(10)

if __name__ == '__main__':
    print("hash :")
    h = input()
    print(create_uid(h))
