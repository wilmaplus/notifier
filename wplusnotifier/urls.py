"""wplusnotifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf.urls import include
from django.contrib import admin
from django.conf import settings
from django.urls import re_path

from wplusnotifier_rest.views import error_404, api_guide


patterns = [
    re_path(r'^api/', include('wplusnotifier_rest.urls')),
    re_path(r'^api/', include('fcmproxy.urls')),
    re_path(r'^$', api_guide),
]

if settings.DJANGO_ADMIN_PANEL:
    patterns.append(re_path(r'^admin/', admin.site.urls))
patterns.append(re_path(r'^', error_404))
urlpatterns = patterns
