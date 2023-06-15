"""
Home Views Configuration
"""
import random
import multiprocessing
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from argon2 import PasswordHasher
from django.core.handlers.wsgi import WSGIRequest
from argon2.exceptions import VerifyMismatchError
from django.core.exceptions import ValidationError
from encsite.middlewares import update_user_last_active, login_required
from .models import User
from . import utils
import json

hasher = PasswordHasher()

@update_user_last_active
def index(req:WSGIRequest):
    uinfo = req.session.get('userinfo')
    if uinfo:
        params = {
            'userinfo': uinfo.copy()
        }
        return render(req,'index.html',params)
    return render(req,'index.html')

def favicon(req):
    return redirect('/static/img/favicon.ico')

@update_user_last_active
def signup(req:WSGIRequest):
    form = req.POST
    if form:
        check = signup_check(req, internal=True)
        name = form.get('name')
        email = form.get('email')
        password = form.get('password')
        check = json.loads(check)
        if check['result'] == 'success':
            gender = str(form.get("gender"))
            gender = gender.lower()
            genders = ['male', 'female']
            if gender not in genders:
                gender = random.choice(genders)
            uid_hash = hasher.hash(email+name[::-2]).split("$")[-1]
            uid = utils.create_uid(uid_hash)
            try:
                new_user = User(
                    name=name,
                    email=email,
                    gender=gender,
                    password=hasher.hash(password+email[::-2]),
                    id=uid
                )
                new_user.clean_fields()
                new_user.save()
                req.session['userinfo'] = {
                    'id' : uid,
                    'name' : name,
                    'email' : email,
                }
                return redirect('home')
            except ValidationError as error:
                err_dict = dict(error)
                err_msg = err_dict.get('email')
                if err_msg:
                    params = {
                        'values' : {
                            'email' : email
                        },
                        'err' : err_msg
                    }
                    return render(req,'signup.html',params)
                else:
                    raise error
        else:
            params = {
                'values':{
                    'email' : email,
                    'name' : name
                },
                'err' : check['message']
            }
            return render(req,'signup.html',params)
    return render(req,"signup.html")

@update_user_last_active
def login(req:WSGIRequest):
    form = req.POST
    if form:
        email = form.get('email')
        password = form.get('password')
        check = login_check(req,internal=True)
        check = json.loads(check)
        if check['result']=='success':
            user = User.objects.get(email=email)
            userinfo = {
                'id' : user.id,
                'name' : user.name,
                'email' : user.email
            }
            req.session['userinfo'] = userinfo
            return redirect('home')
        else:
            params = {
                'values' : {
                    'email' : email,
                    'password': password
                },
                'err' : check['message']
            }
            return render(req,'login.html',params)
    else:
        return render(req,'login.html')

@login_required
@update_user_last_active
def logout(req:WSGIRequest):
    del req.session['userinfo']
    return redirect('home')

# Json responses
def login_check(req:WSGIRequest,internal=False):
    form = req.POST
    wrapper = json.dumps if internal else JsonResponse
    if form:
        email = form.get('email')
        password = form.get('password')
        if None in (email,password):
            return wrapper({
                'result' : 'err',
                'message' : 'Insufficient information to login'
            })
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return wrapper({
                'result' : 'err',
                'message' : 'This email is not associated with any acount'
            })
        else:
            hashed_pass = user.password
            try:
                hasher.verify(hashed_pass,password+email[::-2])
            except VerifyMismatchError:
                return wrapper({
                    'result': 'err',
                    'message': 'The password you provided is incorrect'
                })
            else:
                return wrapper({
                    'result':'success',
                    'message' : 'login credentials verfied'
                })

def signup_check(req:WSGIRequest, internal=False):
    form = req.POST
    wrapper = json.dumps if internal else JsonResponse
    if form:
        p1 = form.get('password')
        p2 = form.get('password2')
        name = form.get('name')
        email = form.get("email")
        gender = form.get("gender")
        if None in (p1,p2,name,email,gender):
            return wrapper({
                "result" : "err",
                "message" : "Insufficient information to create an account"
            })
        try:
            user = User.objects.get(email=email)
            return wrapper({
                "result": "err",
                "message": "This email is already linked with another account"
            })
        except User.DoesNotExist:
            if len(email)>150:
                return wrapper({
                    "result" : "err",
                    "message" : "Email cannot contain more than 150 characters"
                })
            if len(name)>100:
                return wrapper({
                    "result" : "err",
                    "message" : "Name cannot contain more than 100 characters"
                })
            if len(p1)>=8:
                if p1==p2:
                    try:
                        user = User(
                            email = email,
                            name=name,
                        )
                        user.clean_fields()
                    except ValidationError as e:
                        err_dict = dict(e)
                        if 'email' in err_dict.keys():
                            err_msg = err_dict['email'][0]
                            return wrapper({
                                'result':'err',
                                'message' : err_msg
                            })
                else:
                    return wrapper({
                        "result" : "err",
                        'message': "Passwords do not match"
                    })
            else:
                return wrapper({
                    "result":"err",
                    "message": "Password must contain atleast 8 characters"
                })
            return wrapper({
                "result":"success",
                "message": "Valid information, can proceed"
            })
