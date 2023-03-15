"""
Text App Views Configuration
"""
from django.shortcuts import render, redirect

def index(req):
    return render(req,'text/index.html')