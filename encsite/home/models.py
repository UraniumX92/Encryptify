from django.db import models
from image.models import ImageJob

# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=120,primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=150)
    password = models.CharField(max_length=97)
    gender = models.CharField(max_length=6)
    joined_at = models.DateTimeField(auto_now_add=True,editable=True)
    image_jobs = models.ManyToManyField(to=ImageJob,blank=True)
    del_account = models.BooleanField(default=False)
    last_active = models.DateTimeField(null=True,blank=True)

    def dict(self):
        ijobs = list(self.image_jobs.all())
        ijobs = [x.id for x in ijobs]
        return {
            'id' : self.id,
            'name' : self.name,
            'email' : self.email,
            'password' : self.password,
            'gender' : self.gender,
            'joined_at' : self.joined_at,
            'image_jobs' : ijobs,
            'del_account' : self.del_account,
            # 'last_active' self.last_active
        }

    def __str__(self):
        dt_format = "(%d/%b/%Y - %I:%M:%S %p %Z)"
        joined_at = self.joined_at.strftime(dt_format)
        return f"{self.email} , {self.name} , {joined_at}"