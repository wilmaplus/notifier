#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import sys

import requests

if ((3, 0) <= sys.version_info <= (3, 9)):
    from urllib.parse import urlparse
elif ((2, 0) <= sys.version_info <= (2, 9)):
    from urlparse import urlparse
from .classes import *
from django.conf import settings



class WilmaHttpClient:

    def __init__(self, user_auth, wilma_url):
        if wilma_url[len(wilma_url)-1] is not "/":
            wilma_url = wilma_url + "/"
        self.user_auth = user_auth
        self.baseUrl = wilma_url
        self.sessionHttp = requests.Session()

    def getBaseURLDomainName(self):
        return '{uri.netloc}'.format(uri=urlparse(self.baseUrl))

    def get_request(self, url):
        try:
            r = self.sessionHttp.get(self.baseUrl + url)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def authenticated_get_request(self, url):
        sessionCookie = requests.cookies.create_cookie(domain=self.getBaseURLDomainName(), name='Wilma2SID',
                                                       value=self.user_auth)
        self.sessionHttp.cookies.set_cookie(sessionCookie)
        try:
            r = self.sessionHttp.get(self.baseUrl + url)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_request(self, url, data, headers=None, followRedirects=True):
        try:
            r = self.sessionHttp.post(self.baseUrl + url, data=data, allow_redirects=followRedirects)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def authenticated_post_request(self, url, data, followRedirects=True):
        sessionCookie = requests.cookies.create_cookie(domain=self.getBaseURLDomainName(), name='Wilma2SID',
                                                       value=self.user_auth)
        self.sessionHttp.cookies.set_cookie(sessionCookie)

        try:
            r = self.sessionHttp.post(self.baseUrl + url, data=data,
                                      allow_redirects=followRedirects)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)


class FCMHttpClient:

    def __init__(self):
        baseURL = settings.FCM_URL
        if baseURL[len(baseURL) - 1] is not "/":
            baseURL = baseURL + "/"
        self.baseUrl = baseURL
        self.sessionHttp = requests.Session()

    def get_request(self, url):
        try:
            headers = {'Authorization': 'key='+settings.FCM_SERVER_KEY}
            r = self.sessionHttp.get(self.baseUrl + url, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_request(self, url, data, followRedirects=True):
        try:
            headers = {'Authorization': 'key='+settings.FCM_SERVER_KEY}
            r = self.sessionHttp.post(self.baseUrl + url, data=data, allow_redirects=followRedirects, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_json_request(self, url, data, followRedirects=True):
        try:
            headers = {'Authorization': 'key=' + settings.FCM_SERVER_KEY}
            r = self.sessionHttp.post(self.baseUrl + url, json=data, allow_redirects=followRedirects,
                                          headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)


class IIDHttpClient:

    def __init__(self):
        baseURL = settings.IID_URL
        if baseURL[len(baseURL) - 1] is not "/":
            baseURL = baseURL + "/"
        self.baseUrl = baseURL
        self.sessionHttp = requests.Session()

    def get_request(self, url):
        try:
            headers = {'Authorization': 'key='+settings.IID_SERVER_KEY}
            r = self.sessionHttp.get(self.baseUrl + url, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)
