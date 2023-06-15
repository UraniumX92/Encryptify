from django.db import models

# Create your models here.
class ImageJob(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    operation = models.CharField(max_length=7)
    save_job = models.BooleanField(default=False)
    user_name = models.CharField(max_length=100,null=True,blank=True)
    user_id = models.CharField(max_length=120)
    started_at = models.DateTimeField(null=True,blank=True)
    finished_at = models.DateTimeField(null=True,blank=True)
    expires_at = models.DateTimeField(null=True,blank=True)
    visited = models.BooleanField(default=False)
    result_saved = models.BooleanField(default=False)
    protected = models.BooleanField(default=False)
    errs = models.JSONField(default=dict,null=True,blank=True) #to store error messages if there are any

    def status(self):
        return "error" if self.errs else "Finished" if self.result_saved else "Processing"

    def dict(self):
        started_at = self.started_at.timestamp() if self.started_at else None
        finished_at = self.finished_at.timestamp() if self.finished_at else None
        expires_at = self.expires_at.timestamp() if self.expires_at else None
        return {
            'id' : self.id,
            'status' : self.status(),
            'name' : self.name,
            'operation' : self.operation,
            'save_job' : self.save_job,
            'user_name' : self.user_name,
            'user_id' : self.user_id,
            'started_at' : started_at,
            'finished_at' : finished_at,
            'expires_at' : expires_at,
            'visited' : self.visited,
            'result_saved' : self.result_saved,
            'protected' : self.protected,
            'errs'   : self.errs,
            'time_taken' : self.processing_time_str()
        }

    def processing_time(self):
        if self.status() == "Finished" and self.started_at and self.finished_at:
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
        tstarted = self.started_at.strftime(dt_format) if self.started_at else "not started"
        name = self.user_name if self.user_name else ''
        return f"{self.id} - {name} - {self.name} - {tstarted} - {self.status()}"


def get_duration_str(ts):
    second = 1
    minute = second*60
    temp_ts = ts
    ms = f"{(temp_ts - int(temp_ts)):.4f}".split('.')[1]
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