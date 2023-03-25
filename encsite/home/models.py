from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=97)
    gender = models.CharField(max_length=6)
    id = models.CharField(max_length=120,primary_key=True)

    def __str__(self):
        return f"{self.email} , {self.name}"