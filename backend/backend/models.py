# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(primary_key=True, max_length=64)
    password = models.CharField(max_length=64, default='123456')
    email = models.EmailField(default='123456789@gmail.com', unique=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_name', 'email'], name='unique_user')
        ]
    def __unicode__(self):
        return 'Name: ' + self.user_name + ',UID: ' + self.UID

class LabelImg(models.Model):
    img = models.ImageField(upload_to='uploads/', max_length=1000)
    description = models.TextField(max_length=1000, default="NULL")
    status = models.CharField(max_length=20, default="未标注")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
