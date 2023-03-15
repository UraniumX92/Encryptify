"""
Home Views Configuration
"""
from django.shortcuts import render, redirect

def index(request):
    return render(request,'index.html')