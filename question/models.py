from django.db import models

# Create your models here.


class RobotKiller(models.Model):
    id = models.IntegerField(primary_key=True)
    ip = models.CharField(max_length=16)    # ip
    visits = models.IntegerField()          # request times
    time = models.DateTimeField()           # request begin time
    status = models.CharField(max_length=16)
    class Meta:
        db_table = 'robot'
