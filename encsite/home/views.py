"""
Home Views Configuration
"""
import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
from argon2 import PasswordHasher
from django.core.handlers.wsgi import WSGIRequest
from argon2.exceptions import VerifyMismatchError
from django.core.exceptions import ValidationError
from .models import User
from . import utils
import json


hasher = PasswordHasher()

def index(req:WSGIRequest):
    uinfo = req.session.get('userinfo')
    if uinfo:
        params:dict = {
            'userinfo': uinfo.copy()
        }
        return render(req,'index.html',params)
    return render(req,'index.html')


def signup(req:WSGIRequest):
    form = req.POST
    if form:
        check = singup_check(req,internal=True)
        name = form.get('name')
        email = form.get('email')
        password = form.get('password')
        check = json.loads(check)
        if check['result'] == 'success':
            gender = str(form.get("gender"))
            gender = gender.lower()
            genders = ['male', 'female']
            if gender.lower() not in genders:
                gender = random.choice(genders)
            uid = hasher.hash(email+name[::-2]).split("$")[-1]
            uid = f"{str(utils.timenow()).split('.')[0]}{uid}"
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
                    'name' : name,
                    'email' : email,
                }
                return redirect('home')
            except ValidationError as e:
                err_msg = dict(e)['email'][0]
                params = {
                    'values' : {
                        'email' : email
                    },
                    'err' : err_msg
                }
                return render(req,'signup.html',params)
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

def singup_check(req:WSGIRequest,internal=False):
    form = req.POST
    wrapper = json.dumps if internal else JsonResponse
    if form:
        p1 = form.get('password')
        p2 = form.get('password2')
        name = form.get('name')
        email = form.get("email")
        try:
            user = User.objects.get(email=email)
            return wrapper({
                "result": "err",
                "message": "This email is already linked with another account."
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
                    pass # success, data is returned after current if-else ladder.
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