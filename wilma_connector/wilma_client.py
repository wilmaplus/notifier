#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import json

from .http_client import WilmaHttpClient
from .classes import *
from urllib.parse import urlparse

def checkForWilmaError(response):
    if response.status_code != 200:
        jsonResponse = json.loads(response.text)
        errorBody = jsonResponse.get('error', None)
        if errorBody is not None:
            return ErrorResult(Exception(errorBody['message']), errorBody)
        else:
            return ErrorResult(Exception("Unable to parse error code: " + str(response.status_code)))
    else:
        return None


class WilmaClient:

    def __init__(self, wilma_url, wilma_session):
        self.wilma_url = wilma_url
        self.wilma_session = wilma_session
        self.http_client = WilmaHttpClient(wilma_session, wilma_url)

    def checkSession(self):
        requestResult = self.http_client.authenticated_get_request("index_json")
        if requestResult.is_error():
            return requestResult
        error_check = checkForWilmaError(requestResult.get_response())
        if error_check is not None:
            return error_check
        jsonResponse = json.loads(requestResult.get_response().text)
        user_id = jsonResponse.get('PrimusId', -1)
        user_type = jsonResponse.get('Type', -1)
        if user_id is not -1 and user_type is not -1:
            return SessionValidateResult(True, user_id, user_type, urlparse(self.wilma_url).hostname)
        else:
            return ErrorResult('Unable to get user information. Are you sure that you included Slug ID?')

    def getExams(self, check_session=False):
        if check_session:
            session_result = self.checkSession()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        requestResult = self.http_client.authenticated_get_request("exams/index_json")
        if requestResult.is_error():
            return requestResult
        error_check = checkForWilmaError(requestResult.get_response())
        if error_check is not None:
            return error_check
        jsonResponse = json.loads(requestResult.get_response().text)
        exams = jsonResponse.get('Exams', [])
        return ExamsResult(exams)

    def getMessages(self, check_session=False):
        if check_session:
            session_result = self.checkSession()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        requestResult = self.http_client.authenticated_get_request("messages/index_json/all")
        if requestResult.is_error():
            return requestResult
        error_check = checkForWilmaError(requestResult.get_response())
        if error_check is not None:
            return error_check
        jsonResponse = json.loads(requestResult.get_response().text)
        exams = jsonResponse.get('Messages', [])
        return MessagesResult(exams)

    def getObservations(self, check_session=False):
        if check_session:
            session_result = self.checkSession()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        requestResult = self.http_client.authenticated_get_request("attendance/index_json")
        if requestResult.is_error():
            return requestResult
        error_check = checkForWilmaError(requestResult.get_response())
        if error_check is not None:
            return error_check
        jsonResponse = json.loads(requestResult.get_response().text)
        obs = jsonResponse.get('Observations', [])
        savingExcuseAllowed = ('AllowSaveExcuse' in jsonResponse)
        return ObservationsResult(obs, savingExcuseAllowed)

    def getNews(self, check_session=False):
        if check_session:
            session_result = self.checkSession()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        requestResult = self.http_client.authenticated_get_request("news/index_json")
        if requestResult.is_error():
            return requestResult
        error_check = checkForWilmaError(requestResult.get_response())
        if error_check is not None:
            return error_check
        jsonResponse = json.loads(requestResult.get_response().text)
        news = jsonResponse.get('News', [])
        return NewsResult(news)
