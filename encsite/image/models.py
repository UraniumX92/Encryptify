from django.db import models

# Create your models here.
class ImageJob(models.Model):
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
        return f"Finished" if self.finished_at else "Processing"

    def processing_time(self):
        if self.state() == "Finished":
            tstart = self.started_at.timestamp()
            tfinished = self.finished_at.timestamp()
            return tfinished-tstart
        else:
            return -1

    def processing_time_str(self):
        ptime = self.processing_time()
        if ptime>=0:
            return get_duration_str(self.processing_time())
        else:
            return "Job not finished yet"


    def __str__(self):
        dt_format = "(%d/%b/%Y - %I:%M:%S %p %Z)"
        tstarted = self.started_at.strftime(dt_format)
        return f"{self.id} - {self.user_name} - {self.name} - {tstarted} - {self.state()}"


def get_duration_str(ts):
    second = 1
    minute = second*60
    temp_ts = ts
    ms = f"{(temp_ts - int(temp_ts)):.10f}".split('.')[1]
    time_tup = [0,0]
    duration_str = ''
    while temp_ts>=second:
        if temp_ts>minute:
            temp_ts -= minute
            time_tup[0] += 1
        else:
            temp_ts -= second
            time_tup[1] += 1
    if time_tup[0]>0:
        duration_str += f"{time_tup[0]} minute(s) and "
    if time_tup[1]>=0:
        duration_str += f"{time_tup[1]}"
    duration_str += f".{ms} seconds"
    return duration_str