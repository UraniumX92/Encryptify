"""
Image App URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='image'),
    # Form views
    path('encryption/',views.encryption,name='img_encryption'),
    path('steganos/',views.steganography,name='img_steganos'),
    # Tasks Display views
    path('encryption/tasks/<int:job_id>/',views.enc_serve,name="img_enc_serve"),
    path('steganos/tasks/<int:job_id>/',views.stg_serve,name='img_stg_serve'),
    # Job File views
    path('encryption/job/<int:job_id>/',views.enc_attachment,name='img_enc_attachment'),
    path('steganos/job/<int:job_id>/',views.stg_attachment,name='img_stg_attachment'),
    # Info view
    path('<job_type>/info/<int:job_id>/',views.get_job_info,name='img_get_info'),
]
