"""
Text App URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='text'),
    # Form Views
    path('vigenere_plus/',views.vigenere,name="vigenere_plus"),
    path('scramble/',views.scramble,name="scramble"),
    path('binary/',views.binary,name="binary"),
    # AJAX JSON Responses
    path('vgplus/',views.vgplus,name="vgplus"),
    path('scrx/',views.scrx,name="scrx"),
    path('binx/',views.binx,name="binx"),

]
