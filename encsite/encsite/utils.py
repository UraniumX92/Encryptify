from django.utils import timezone
from datetime import datetime
from dotenv import load_dotenv
from home.models import User
import os
load_dotenv()
envs = os.environ

def timenow():
    """
    Current datetime
    :return: datetime
    """
    return datetime.now(tz=timezone.utc)

def last_active_thr(uid):
    try:
        user = User.objects.get(id=uid)
        user.last_active = timenow()
        user.save()
    except User.DoesNotExist:
        pass