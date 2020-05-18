#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import json
import urllib

from .http_client import IIDHttpClient
from .classes import *



def checkForIIDError(response):
    if response.status_code != 200:
        jsonResponse = json.loads(response.text)
        errorBody = jsonResponse.get('error', None)
        if errorBody is not None:
            return ErrorResult(Exception(errorBody))
        else:
            return ErrorResult(Exception("Unable to parse error code: " + str(response.status_code)))
    else:
        return None


class IIDClient:

    def __init__(self):
        self.http_client = IIDHttpClient()

    def push_key_details(self, push_key):
        requestResult = self.http_client.get_request("iid/info/"+push_key)
        if requestResult.is_error():
            return requestResult
        try:
            error_check = checkForIIDError(requestResult.get_response())
            if error_check is not None:
                return error_check
            jsonResponse = json.loads(requestResult.get_response().text)
            return PushDetailsRequest(jsonResponse)
        except json.JSONDecodeError:
            if requestResult.get_response().status_code == 404:
                return ErrorResult('Invalid iid_key!')
            else:
                return ErrorResult("Couldn't parse JSON response")
