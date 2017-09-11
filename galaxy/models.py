from django.db import models

# Create your models here.


class Galaxy(models.Model):
    id = models.AutoField(primary_key=True)  # auto increment
    ip = models.CharField(max_length=16)  # ip
    post_img = models.CharField(max_length=128)  # posted img url
    question_ids = models.CharField(max_length=64)  # returned questions ids
    upload_time = models.DateTimeField()  # request time

    class Meta:
        db_table = 'user_data'
        app_label = 'galaxy'