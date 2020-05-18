"""wplusnotifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from wplusnotifier_rest.views import error_404, api_guide


patterns = [
    url(r'^api/', include('wplusnotifier_rest.urls')),
    url(r'^$', api_guide),
    url(r'^', error_404),
]

if settings.DJANGO_ADMIN_PANEL:
    patterns.append(url(r'^admin/', admin.site.urls))
urlpatterns = patterns
