from datetime import datetime


bullet_char = "\u2022"
# ----------------------------------- #

def timenow():
    """
    Current timestamp
    :return: float - timestamp
    """
    return datetime.now().timestamp()