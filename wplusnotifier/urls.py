"""wplusnotifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings

patterns = [
    url('api/v1/', include('wplusnotifier_rest.urls'))
]

if settings.ADMIN_PANEL:
    patterns.append(url(r'^admin/', admin.site.urls))
urlpatterns = patterns
