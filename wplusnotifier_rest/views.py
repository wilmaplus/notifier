# -*- coding: utf-8 -*-

#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import *
from wilma_connector.wilma_client import WilmaClient
from wilma_connector.classes import ErrorResult


@api_view(['POST'])
@permission_classes([])
def push(request):
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'))
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'))
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.checkSession()
    if session_check.is_error():
        return generateErrorResponse(session_check)
    else:
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
