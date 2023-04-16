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
    path('signupcheck', views.signup_check, name='signupcheck'),
    path('logincheck',views.login_check,name='logincheck'),
    # temp
    path('a',views.a,name='a'),
    path('asdf',views.redr,name='redr'),
    path('json/<param>/<int:param2>',views.ptest,name='ptest'),
    path('test',views.test,name='test')
]
