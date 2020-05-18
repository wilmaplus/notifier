# -*- coding: utf-8 -*-

#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import *

from routine_runner.runner import *
from wilma_connector.classes import ErrorResult
from wilma_connector.iid_client import IIDClient
from wilma_connector.wilma_client import WilmaClient


@api_view(['POST'])
@permission_classes([])
def push(request):
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
