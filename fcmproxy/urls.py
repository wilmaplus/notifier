#  Copyright (c) 2022 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.urls import re_path
from rest_framework import routers

from fcmproxy.views import add, remove

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    re_path(r'^proxy/v1/add', add),
    re_path(r'^proxy/v1/remove', remove),
]