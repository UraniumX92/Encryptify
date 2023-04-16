"""
Image App Views Configuration
"""
from django.shortcuts import render, redirect

def index(request):
    uinfo = request.session.get('userinfo')
    if uinfo:
        params = {
            'userinfo': uinfo.copy()
        }
        return render(request,'image/ilanding.html',params)
    return render(request,'image/ilanding.html')

def encryption(request):
    uinfo = request.session.get('userinfo')
    if uinfo:
        params = {
            'userinfo' : uinfo.copy()
        }
        return render(request,'image/encryption.html',params)
    return render(request,'image/encryption.html')