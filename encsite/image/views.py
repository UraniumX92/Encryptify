"""
Image App Views Configuration
"""
from django.shortcuts import render, redirect

def index(req):
    return render(req,'image/index.html')