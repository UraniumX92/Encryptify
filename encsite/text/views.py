"""
Text App Views Configuration
"""
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.core.exceptions import PermissionDenied, BadRequest
from encsite.middlewares import update_user_last_active
from . import enc_utils
from . import binary_utils
from . import utils

@update_user_last_active
def index(req):
    uinfo = req.session.get('userinfo')
    params = {}
    if uinfo:
        params:dict = {
            'userinfo': uinfo.copy()
        }
    return render(req,'text/tlanding.html',params)

# Form Views
@update_user_last_active
def vigenere(req):
    uinfo = req.session.get('userinfo')
    params = {}
    if uinfo:
        params = {
            'userinfo' : uinfo.copy()
        }
    return render(req,'text/vigenere.html',params)

@update_user_last_active
def xor(req):
    uinfo = req.session.get('userinfo')
    params = {}
    if uinfo:
        params = {
            'userinfo': uinfo.copy()
        }
    return render(req, 'text/xor.html', params)

@update_user_last_active
def scramble(req):
    uinfo = req.session.get('userinfo')
    params = {}
    if uinfo:
        params = {
            'userinfo' : uinfo.copy()
        }
    return render(req,'text/scramble.html',params)

@update_user_last_active
def binary(req):
    uinfo = req.session.get('userinfo')
    params = {}
    if uinfo:
        params = {
            'userinfo' : uinfo.copy()
        }
    return render(req,'text/binary.html',params)

# AJAX JSON Responses
@update_user_last_active
def vgplus(req):
    form = req.POST
    if form:
        text = form.get("text")
        key = form.get("key")
        op = form.get("op")
        if any(not x for x in (text,key,op)):
            return JsonResponse({
                'status' : 400,
                'err' : "Please fill all the required info"
            })
        key = utils.get_key(key)
        if op=='encrypt':
            rtext = enc_utils.ciph(text,key)
            return JsonResponse({
                'status' : 200,
                'text' : rtext
            })
        else:
            rtext = enc_utils.deciph(text,key)
            return JsonResponse({
                'status' : 200,
                'text' : rtext
            })
    else:
        return JsonResponse({
            'status' : 400,
            'err' : "Bad Request"
        })

@update_user_last_active
def xorx(req):
    form = req.POST
    if form:
        text = form.get("text").encode('utf-16')
        text = text.decode('utf-16')
        key = form.get("key")
        if any(not x for x in (text, key)):
            return JsonResponse({
                'status': 400,
                'err': "Please fill all the required infox"
            })
        key = utils.get_key(key)
        rtext = enc_utils.xor_text(text, key).encode('utf-16')
        rtext = rtext.decode('utf-16')
        return JsonResponse({
            'status': 200,
            'text': rtext
        })
    else:
        return JsonResponse({
            'status': 400,
            'err': "Bad Request"
        })

@update_user_last_active
def scrx(req):
    form = req.POST
    if form:
        text = form.get("text")
        key = form.get("key")
        op = form.get("op")
        if any(not x for x in (text, key, op)):
            return JsonResponse({
                'status': 400,
                'err': "Please fill all the required info"
            })
        key = utils.get_key(key)
        if op == 'encrypt':
            rtext = enc_utils.scrambler(text, key)
            return JsonResponse({
                'status': 200,
                'text': rtext
            })
        else:
            rtext = enc_utils.unscramber(text, key)
            return JsonResponse({
                'status': 200,
                'text': rtext
            })
    else:
        return JsonResponse({
            'status': 400,
            'err': "Bad Request"
        })

@update_user_last_active
def binx(req):
    form = req.POST
    if form:
        text = form.get("text")
        op = form.get("op")
        if any(not x for x in (text, op)):
            return JsonResponse({
                'status': 400,
                'err': "Please fill all the required info"
            })
        if op == 'encrypt':
            rtext = binary_utils.text_to_binary(text)
            return JsonResponse({
                'status': 200,
                'text': rtext
            })
        else:
            try:
                rtext = binary_utils.binary_to_text(text)
            except ValueError :
                return JsonResponse({
                    'status' : 400,
                    'err' : "Given text is not binary text, Binary text only consists of 0s and 1s (Might contain spaces)"
                })
            else:
                return JsonResponse({
                    'status': 200,
                    'text': rtext
                })
    else:
        return JsonResponse({
            'status': 400,
            'err': "Bad Request"
        })