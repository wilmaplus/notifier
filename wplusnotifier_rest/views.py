# -*- coding: utf-8 -*-

#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import *

from routine_runner.runner import *
from wilma_connector.classes import ErrorResult, RequestResult
from wilma_connector.iid_client import IIDClient
from wilma_connector.wilma_client import WilmaClient


# Custom Error handler to make it fit with rest of the API
def custom_exception_handler(exc, context):
    return generateErrorResponse(ErrorResult(exc))


def checkApiKey(request):
    if settings.API_KEY_CHECK_ENABLED:
        post_key = request.data.get('apikey', None)
        get_key = request.GET.get('apikey', None)
        apikey = None
        if post_key is not None:
            apikey = post_key
        elif get_key is not None:
            apikey = get_key
        if apikey is None:
            return ErrorResult('apikey is missing!')
        else:
            if apikey not in settings.API_KEYS:
                return ErrorResult('Invalid apikey!')
    return RequestResult(False)


@api_view(['POST'])
@permission_classes([])
def push(request):
    apikey_result = checkApiKey(request)
    if apikey_result.is_error():
        return generateErrorResponse(apikey_result)
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    iid_key = request.data.get('iid_key', None)
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'))
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'))
    if iid_key is None:
        return generateErrorResponse(ErrorResult('iid_key is missing!'))
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.checkSession()
    if session_check.is_error():
        return generateErrorResponse(session_check)
    else:
        iid_client = IIDClient()
        iid_result = iid_client.push_key_details(iid_key)
        if iid_result.is_error():
            return generateErrorResponse(iid_result)
        else:
            details = iid_result.get_details()
            if settings.VALIDATE_CLIENT_KEY:
                if not details.get('application', None) in settings.VALID_CLIENT_PACKAGES:
                    return generateErrorResponse(ErrorResult('iid_key is not trusted for this notifier!'))
        runRoutines(server_url, session_cookies, iid_key, session_check.get_combined_user_id())
        return generateResponse({})


def generateErrorResponse(error_result):
    return generateError(str(error_result.get_exception()))


def generateError(cause):
    base = baseResponse()
    base.update({'cause': cause})
    return Response(base)


def generateResponse(data):
    base = baseResponse(True)
    base.update(data)
    return Response(base)


def baseResponse(status=False):
    return {
        'status': status
    }
