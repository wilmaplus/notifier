
#  Copyright (c) 2020 openKirkes, developed by Developer From Jokela

from django.conf.urls import url, include
from rest_framework import routers

from .views import push

router = routers.DefaultRouter()

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url('', include(router.urls)),
    url(r'^push', push),
]
