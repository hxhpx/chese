
# Create your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class History(models.Model):
    #id = models.SmallIntegerField()
    name = models.CharField(max_length=50)
    time = models.DateTimeField(auto_now=True)
    size = models.SmallIntegerField()
    stepCnt = models.SmallIntegerField()
    list = models.TextField()

    def __unicode__(self):
        return self.name, self.time, self.size, self.stepCnt, self.list


class Size(models.Model):
    size = models.SmallIntegerField()

    def __unicode__(self):
        return self.size