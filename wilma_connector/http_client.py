#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import os.path
import jwt
import requests
from urllib.parse import urlparse
from .classes import *
from django.conf import settings
from datetime import datetime
import calendar
import uuid


class WilmaHttpClient:

    def __init__(self, user_auth, wilma_url):
        if wilma_url[len(wilma_url) - 1] != "/":
            wilma_url = wilma_url + "/"
        self.user_auth = user_auth
        self.baseUrl = wilma_url
        self.sessionHttp = requests.Session()

    def getBaseURLDomainName(self):
        return '{uri.netloc}'.format(uri=urlparse(self.baseUrl))

    def get_plain_url(self):
        return '{uri.scheme}://{uri.hostname}'.format(uri=urlparse(self.baseUrl))

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
        if baseURL[len(baseURL) - 1] != "/":
            baseURL = baseURL + "/"
        self.baseUrl = baseURL
        self.sessionHttp = requests.Session()

    def get_request(self, url):
        try:
            headers = {'Authorization': 'key=' + settings.FCM_SERVER_KEY}
            r = self.sessionHttp.get(self.baseUrl + url, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_request(self, url, data, followRedirects=True):
        try:
            headers = {'Authorization': 'key=' + settings.FCM_SERVER_KEY}
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


def generate_apns_authentication_token():
    with open(os.path.join(settings.BASE_DIR, settings.APNS_PRIVATE_KEY_FILENAME), "r") as key_file:
        apns_private_key = key_file.read()
    unix_timestamp = calendar.timegm(datetime.utcnow().utctimetuple())
    return jwt.encode({"iss": settings.APPLEDEV_TEAM_ID, "iat": unix_timestamp}, apns_private_key,
                      algorithm="ES256", headers={"kid": settings.APNS_KEY_ID})


class APNSHttpClient:

    def __init__(self):
        baseURL = settings.APNS_SERVER_URL
        if baseURL[len(baseURL) - 1] != "/":
            baseURL = baseURL + "/"
        self.baseUrl = baseURL
        self.sessionHttp = requests.Session()

    def get_request(self, url):
        try:
            headers = {'Authorization': 'Bearer {}'.format(generate_apns_authentication_token())}
            r = self.sessionHttp.get(self.baseUrl + url, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_request(self, url, data, push_type, apns_expiration, apns_priority, apns_topic, follow_redirects=True):
        try:
            headers = {
                'authorization': 'bearer {}'.format(generate_apns_authentication_token()),
                'apns-push-type': push_type,
                'apns-id': str(uuid.uuid4()),
                'apns-expiration': str(apns_expiration),
                'apns-priority': str(apns_priority),
                'apns-topic': apns_topic,
            }
            r = self.sessionHttp.post(self.baseUrl + url, data=data, allow_redirects=follow_redirects, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)

    def post_json_request(self, url, data, push_type, apns_expiration, apns_priority, apns_topic, follow_redirects=True):
        try:
            headers = {
                'authorization': 'bearer {}'.format(generate_apns_authentication_token()),
                'apns-push-type': push_type,
                'apns-id': str(uuid.uuid4()),
                'apns-expiration': str(apns_expiration),
                'apns-priority': str(apns_priority),
                'apns-topic': apns_topic,
            }
            r = self.sessionHttp.post(self.baseUrl + url, json=data, allow_redirects=follow_redirects,
                                      headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)


class IIDHttpClient:

    def __init__(self):
        baseURL = settings.IID_URL
        if baseURL[len(baseURL) - 1] != "/":
            baseURL = baseURL + "/"
        self.baseUrl = baseURL
        self.sessionHttp = requests.Session()

    def get_request(self, url):
        try:
            headers = {'Authorization': 'key=' + settings.IID_SERVER_KEY}
            r = self.sessionHttp.get(self.baseUrl + url, headers=headers)
            return RequestResult(False, None, r)
        except Exception as e:
            return ErrorResult(e)
