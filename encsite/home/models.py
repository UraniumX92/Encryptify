from django.db import models
from image.models import ImageJob
from text.models import TextJob

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=120,primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=97)
    gender = models.CharField(max_length=6)
    joined_at = models.DateTimeField(auto_now_add=True,editable=True)
    text_jobs = models.ManyToManyField(to=TextJob,blank=True)
    image_jobs = models.ManyToManyField(to=ImageJob,blank=True)

    def dict(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password' : self.password,
            'gender' : self.gender,
            'joined_at' : self.joined_at,
            'text_jobs' : self.text_jobs,
            'image_jobs' : self.image_jobs
        }

    def __str__(self):
        return f"{self.email} , {self.name}"