"""
Home Views Configuration
"""
import random
from datetime import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from argon2 import PasswordHasher
from django.core.handlers.wsgi import WSGIRequest
from argon2.exceptions import VerifyMismatchError
from django.core.exceptions import ValidationError
from .models import User
from . import utils
import json

# temp
from image.models import ImageJob

hasher = PasswordHasher()

def index(req:WSGIRequest):
    uinfo = req.session.get('userinfo')
    if uinfo:
        params = {
            'userinfo': uinfo.copy()
        }
        return render(req,'index.html',params)
    return render(req,'index.html')


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


def a(req):
    uinfo = req.session['userinfo']
    username = uinfo['name']
    email = uinfo['email']
    user = User.objects.get(email=email)
    ex = datetime.now().timestamp() + (((60*60)*24)*7)
    ex = datetime.fromtimestamp(ex)
    job = ImageJob(
        name='steganos',
        user_name=username,
        user_id=user.id,
        expires_at=ex,
    )
    job.save()
    user.image_jobs.add(job)
    user.save()
    return JsonResponse({
        'result': f'success, added image job to user \'{username}\''
    })

def redr(req):
    p1 = random.choice(['hello','Hi','Random','Django'])
    p2 = random.randint(100,999)
    params = {
        'param' : p1,
        'param2' : p2
    }
    return redirect('ptest',**params)

def ptest(req,param,param2):
    return JsonResponse({
        'result' : 'success',
        'params' : {
            'param' : param,
            'type_param' : str(type(param)),
            'param2' : param2,
            'type_param2' : str(type(param2))
        }
    })

def test(req:WSGIRequest):
    uinfo = req.session['userinfo']
    email = uinfo['email']
    # user = User.objects.get(email=email)
    # jobs = user.image_jobs.all()
    # count = user.image_jobs.count()
    # job = jobs[0]
    # job.delete()
    # print(jobs)
    # print(count)
    # jobs = user.image_jobs.all()
    # count = user.image_jobs.count()
    # print(jobs)
    # print(count)

    user = User.objects.get(id=uinfo['id'])
    print('----------',user.dict(),'----------')
    jobs = user.image_jobs.all()
    print(user.image_jobs.count())
    print(jobs)
    for job in jobs:
        print(f"{job} |||| {job.processing_time()} |||| {job.user_set.all()}")
    # job = ImageJob.objects.get(user_id=uinfo['id'])
    # job.delete()
    # print(job.user_set.all()) #get user from job

    # username = uinfo['name']
    # user = User.objects.get(email=email)
    # ex = datetime.now().timestamp() + (((60*60)*24)*7)
    # ex = datetime.fromtimestamp(ex)
    # job = ImageJob(
    #     job_name='steganos',
    #     user_name=username,
    #     user_id=user.id,
    #     expiry_time=ex,
    # )
    # job.save()
    # user.image_jobs.add(job)
    # user.save()
    return JsonResponse({
        'result' : 'success, check db'
    })
    # return JsonResponse({
    #     'result' : 'Nothing in test'
    # })

# Todo: on website, mention that the only resultant images/texts will be stored in backend, the original images and texts won't be saved.
#   make this very clear.