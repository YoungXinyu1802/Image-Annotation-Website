# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pathlib import Path
import os

MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent.parent, 'backend/Admin')
# Create your models here.
class UserInfo(models.Model):
    user_name = models.CharField(primary_key=True, max_length=64)
    password = models.CharField(max_length=64, default='123456')
    email = models.EmailField(default='123456789@gmail.com', unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_name', 'email'], name='unique_user')
        ]
    # def __unicode__(self):
    #     return 'Name: ' + self.user_name + ',UID: ' + self.UID
    def __str__(self):
        return self.user_name

class Task(models.Model):
    publish_user = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE, related_name='publish_task')
    task_name = models.CharField(max_length=20, default="NULL")
    description = models.TextField(max_length=1000, default="NULL")
    claim_user = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE, related_name='claim_task')
    status = models.CharField(max_length=20, default="未领取")


def getURL(instance, filename):
    imgName = instance.publish_user.user_name
    print(imgName)
    return MEDIA_ROOT + '/%s/database/%s' % (imgName, filename)

class LabelImg(models.Model):
    publish_user = models.ForeignKey(UserInfo, null=True, on_delete=models.CASCADE, related_name='user_img')
    status = models.CharField(max_length=20, default="未标注")
    task_name = models.ForeignKey(Task, null=True, on_delete=models.CASCADE, related_name='img_task')
    img = models.ImageField(upload_to=getURL, max_length=1000)
