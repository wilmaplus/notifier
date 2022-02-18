#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.contrib import admin
from fcmproxy.models import PersistentId, ForwardingSubscriber, SubscriberDevice

admin.site.register(PersistentId)
admin.site.register(ForwardingSubscriber)
admin.site.register(SubscriberDevice)