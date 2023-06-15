"""
Home URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='home'),
    path('favicon.ico',views.favicon,name='favicon'),
    path('signup/', views.signup, name='signup'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('signupcheck/', views.signup_check, name='signupcheck'),
    path('logincheck/',views.login_check,name='logincheck'),
]
