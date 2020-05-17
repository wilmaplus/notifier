#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import requests
from urllib.parse import urlparse
from .classes import *


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

    def post_request(self, url, data, headers=None, followRedirects=True):
        try:
            r = self.sessionHttp.post(self.baseUrl + url, data=data, allow_redirects=followRedirects)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)
