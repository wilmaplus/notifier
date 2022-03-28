#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app
import json

from .http_client import WilmaHttpClient
from .classes import *


def checkForWilmaError(response):
    if response.status_code != 200:
        json_response = json.loads(response.text)
        errorBody = json_response.get('error', None)
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

    def check_session(self):
        request_result = self.http_client.authenticated_get_request("index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        user_id = json_response.get('PrimusId', -1)
        user_type = json_response.get('Type', -1)
        wilma_id = json_response.get('WilmaId', None)
        form_key = json_response.get('FormKey', None)
        if user_id != -1 and user_type != -1 and wilma_id != None:
            return SessionValidateResult(True, user_id, user_type, wilma_id, form_key)
        else:
            return ErrorResult('Unable to get user information. Are you sure that you included Slug ID?')

    def check_global_session(self):
        request_result = self.http_client.authenticated_get_request("index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        user_id = json_response.get('PrimusId', -1)
        user_type = json_response.get('Type', -1)
        wilma_id = json_response.get('WilmaId', None)
        form_key = json_response.get('FormKey', None)
        if user_id != -1 and user_type != -1 and wilma_id != None:
            return GlobalValidateResult(True, user_id, user_type, wilma_id, form_key, [])
        else:
            roles = json_response.get('Roles', [])
            if len(roles) > 0:
                main_account_list = list(filter(lambda x: x['Type'] == 7, roles))
                other_roles_list = list(filter(lambda x: x['Type'] != 7, roles))
                if len(main_account_list) > 0:
                    main_account = main_account_list[0]
                    user_id = main_account['PrimusId']
                    user_type = main_account['Type']
                    form_key = main_account['FormKey']
                return GlobalValidateResult(True, user_id, user_type, wilma_id, form_key, other_roles_list)
            return ErrorResult('Unable to get user information. Are you sure that you included Slug ID?')

    def key_add_request(self, form_key, key):
        request_result = self.http_client.authenticated_post_request("notifyuri",
                                                                     {"formkey": form_key, "PrimaryChannel": key,
                                                                      "PrimaryChannelId": "", "DeviceType": 4})
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        return PushSendRequest(True)

    def key_remove_request(self, form_key, key):
        request_result = self.http_client.authenticated_post_request("notifyuri",
                                                                     {"formkey": form_key, "remove_live_id": "",
                                                                      "PrimaryChannel": key})
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        return PushSendRequest(True)

    def add_push_key(self, key):
        session_info = self.check_global_session()
        if session_info.is_error():
            return session_info
        return self.key_add_request(session_info.form_key, key)

    def remove_push_key(self, key):
        session_info = self.check_global_session()
        if session_info.is_error():
            return session_info
        return self.key_remove_request(session_info.form_key, key)

    def get_exams(self, check_session=False):
        if check_session:
            session_result = self.check_session()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        request_result = self.http_client.authenticated_get_request("exams/index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        exams = json_response.get('Exams', [])
        return ExamsResult(exams)

    def get_messages(self, check_session=False):
        if check_session:
            session_result = self.check_session()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        request_result = self.http_client.authenticated_get_request("messages/index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        exams = json_response.get('Messages', [])
        return MessagesResult(exams)

    def get_observations(self, check_session=False):
        if check_session:
            session_result = self.check_session()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        request_result = self.http_client.authenticated_get_request("attendance/index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        obs = json_response.get('Observations', [])
        saving_excuse_allowed = ('AllowSaveExcuse' in json_response)
        return ObservationsResult(obs, saving_excuse_allowed)

    def get_news(self, check_session=False):
        if check_session:
            session_result = self.check_session()
            if session_result.is_error():
                return session_result
            if not session_result.is_valid_session():
                return ErrorResult(Exception('Invalid session!'))
        request_result = self.http_client.authenticated_get_request("news/index_json")
        if request_result.is_error():
            return request_result
        error_check = checkForWilmaError(request_result.get_response())
        if error_check is not None:
            return error_check
        json_response = json.loads(request_result.get_response().text)
        news = json_response.get('News', [])
        return NewsResult(news)
