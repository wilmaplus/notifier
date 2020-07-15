
#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf.urls import url
from rest_framework import routers

from .views import push, delete

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^v1/push', push),
    url(r'^v1/delete', delete),
]
