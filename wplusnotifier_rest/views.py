# -*- coding: utf-8 -*-

#  Copyright (c) 2020 wilmaplus-notifier, developed by Developer From Jokela, for Wilma Plus mobile app

from __future__ import unicode_literals

from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import *

from routine_runner.runner import *
from wilma_connector.classes import ErrorResult, RequestResult
from wilma_connector.iid_client import IIDClient
from wilma_connector.wilma_client import WilmaClient
import logging


logging.basicConfig(level=logging.DEBUG if settings.DEBUG else logging.WARNING)
logger = logging.getLogger(__name__)

# Custom Error handler to make it fit with rest of the API
def custom_exception_handler(exc, context):
    if settings.DEBUG:
        logger.exception(exc)
        print(exc)
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


@api_view(['GET'])
@permission_classes([])
def error_404(request):
    return generateErrorResponse(ErrorResult("Resource not found"), 404)


@api_view(['POST'])
@permission_classes([])
def push(request):
    apikey_result = checkApiKey(request)
    if apikey_result.is_error():
        return generateErrorResponse(apikey_result)
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    iid_key = request.data.get('iid_key', None)
    routinesToSkip = request.POST.getlist('skip_routine[]')
    if not isinstance(routinesToSkip, list):
        routinesToSkip = [str(routinesToSkip)]
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'), 400)
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'), 400)
    if iid_key is None:
        return generateErrorResponse(ErrorResult('iid_key is missing!'), 400)
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.check_session()
    if session_check.is_error():
        return generateWilmaErrorResponse(session_check, session_check.get_wilma_error())
    else:
        iid_client = IIDClient()
        iid_result = iid_client.push_key_details(iid_key)
        if iid_result.is_error():
            if settings.VALIDATE_CLIENT_KEY:
                return generateErrorResponse(iid_result)
        else:
            details = iid_result.get_details()
            if settings.VALIDATE_CLIENT_KEY:
                if not details.get('application', None) in settings.VALID_CLIENT_PACKAGES:
                    return generateErrorResponse(ErrorResult('iid_key is not trusted for this notifier!'), 400)
        runRoutines(server_url, session_cookies, iid_key, session_check.get_combined_user_id(), routinesToSkip)
        return generateResponse({})


@api_view(['POST'])
@permission_classes([])
def delete(request):
    apikey_result = checkApiKey(request)
    if apikey_result.is_error():
        return generateErrorResponse(apikey_result)
    session_cookies = request.data.get('session', None)
    server_url = request.data.get('server_url', None)
    iid_key = request.data.get('iid_key', None)
    if server_url is None:
        return generateErrorResponse(ErrorResult('server_url is missing!'), 400)
    if session_cookies is None:
        return generateErrorResponse(ErrorResult('session is missing!'), 400)
    if iid_key is None:
        return generateErrorResponse(ErrorResult('iid_key is missing!'), 400)
    wilma_client = WilmaClient(server_url, session_cookies)
    session_check = wilma_client.check_session()
    if session_check.is_error():
        return generateWilmaErrorResponse(session_check, session_check.get_wilma_error())
    else:
        iid_client = IIDClient()
        iid_result = iid_client.push_key_details(iid_key)
        if iid_result.is_error():
            return generateErrorResponse(iid_result)
        else:
            details = iid_result.get_details()
            if settings.VALIDATE_CLIENT_KEY:
                if not details.get('application', None) in settings.VALID_CLIENT_PACKAGES:
                    return generateErrorResponse(ErrorResult('iid_key is not trusted for this notifier!'), 400)
        deleteRoutineFiles(iid_key, session_check.get_combined_user_id())
        return generateResponse({})


def generateErrorResponse(error_result, error_code=500):
    if settings.DEBUG:
        print(error_result.get_exception())
    return generateError(str(error_result.get_exception()), error_code)


def generateWilmaErrorResponse(error_result, wilma_response, error_code=500):
    if wilma_response is not None:
        return generateWilmaError(str(error_result.get_exception()), wilma_response, error_code)
    else:
        return generateError(str(error_result.get_exception()), error_code)


def generateError(cause, error_code=500):
    if settings.DEBUG:
        print(cause)
    base = baseResponse()
    base.update({'cause': cause})
    return Response(base, error_code)


def generateWilmaError(cause, wilma_error, error_code=500):
    base = baseResponse()
    base.update({'cause': cause, 'wilma': wilma_error})
    return Response(base, error_code)


def generateResponse(data):
    base = baseResponse(True)
    base.update(data)
    return Response(base)


def baseResponse(status=False):
    return {
        'status': status
    }


@api_view(['GET'])
@permission_classes([])
def api_guide(request):
    guide_content = {
        "api_name": "wilmaplus-notifier_rest",
        "documentation": settings.DOCUMENTATION_URL,
        "apikey_required": settings.API_KEY_CHECK_ENABLED
    }
    return generateResponse({
        "details": guide_content
    })
