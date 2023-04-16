from django.db import models

# Create your models here.
class TextJob(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    operation = models.CharField(max_length=7)
    save_job = models.BooleanField(default=False)
    state = models.IntegerField()
    user_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=120)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)

    def state(self):
        return "Finished" if self.finished_at else "Processing"

    def __str__(self):
        dt_format = "(%d/%b/%Y - %I:%M:%S %p %Z)"
        tstarted = self.started_at.strftime(dt_format)
        return f"{self.id} - {self.user_name} - {self.name} - {tstarted} - {self.state()}"