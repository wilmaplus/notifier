#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.db import models


class PersistentId(models.Model):
    id = models.AutoField(primary_key=True)
    persistent_id = models.TextField(max_length=50)


class ForwardingSubscriber(models.Model):
    class Meta:
        unique_together = ('wilma_url', 'wilma_uid', 'wilma_usertype'),

    id = models.AutoField(primary_key=True)
    wilma_url = models.TextField()
    wilma_uid = models.TextField()
    wilma_usertype = models.TextField()


class SubscriberDevice(models.Model):
    id = models.AutoField(primary_key=True)
    subscribers = models.ManyToManyField(ForwardingSubscriber)
    type = models.IntegerField()
    key = models.TextField()
