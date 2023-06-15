"""
Site Middlewares
"""
import threading
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from django.core.exceptions import ValidationError
from . import utils
import json

def login_required(view):
    def no_auth(*args,**kwargs):
        rdr = kwargs.get('middleware_redirect')
        if rdr:
            return redirect(rdr)
        return redirect('home')

    def decorated(*args,**kwargs):
        req = args[0]
        uinfo = req.session.get('userinfo')
        if uinfo:
            try:
                id = uinfo['id']
                req_email = uinfo['email']
                req_name = uinfo['name']
                user = utils.User.objects.get(id=id)
                uemail = user.email
                uname = user.name
                if [req_name,req_email] == [uname,uemail]:
                    return view(*args,**kwargs)
                else:
                    kwargs['middleware_redirect'] = '/logout'
                    return no_auth(*args,**kwargs)
            except utils.User.DoesNotExist:
                kwargs['middleware_redirect'] = '/logout'
                return no_auth(*args,**kwargs)
        else:
            return no_auth(*args,**kwargs)
    return decorated

def update_user_last_active(view):
    def decorated(*args,**kwargs):
        result = view(*args,**kwargs)
        req = args[0]
        uinfo = req.session.get('userinfo')
        if uinfo:
            uid = uinfo.get('id')
            thr = threading.Thread(target=utils.last_active_thr,args=[uid])
            thr.start()
        return result
    return decorated