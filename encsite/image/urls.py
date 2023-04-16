"""
Image App URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='image'),
    path('encryption',views.encryption,name='encryption')
]
