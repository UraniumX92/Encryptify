"""
Home URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('signup', views.signup, name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('signupcheck',views.singup_check,name='signupcheck'),
    path('logincheck',views.login_check,name='logincheck')
]
