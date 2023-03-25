"""
Text App Views Configuration
"""
from django.shortcuts import render, redirect

def index(req):
    uinfo = req.session.get('userinfo')
    if uinfo:
        params:dict = {
            'userinfo': uinfo.copy()
        }
        return render(req,'text/index.html',params)
    return render(req,'text/index.html')